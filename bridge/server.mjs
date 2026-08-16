import express from "express";
import TurndownService from "turndown";
import * as htmlparser2 from "htmlparser2";

const app = express();
app.use(express.json({ limit: "50mb" }));

// CORS
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization, x-api-key, anthropic-version, anthropic-beta");
  if (req.method === "OPTIONS") return res.sendStatus(204);
  next();
});

const PROXY_PORT = 4000;
const ZEN_BASE = "https://opencode.ai/zen/v1";
const LOCAL_KEY = "local-master-key";
const turndown = new TurndownService({ headingStyle: "atx", codeBlockStyle: "fenced" });

// Auth - accept any key
app.use((req, res, next) => { next(); });

// Models endpoint
function handleModels(req, res) {
  res.json({
    object: "list",
    data: [
      { id: "opencode/deepseek-v4-flash-free", object: "model" },
      { id: "opencode/mimo-v2.5-free", object: "model" },
      { id: "opencode/nemotron-3-ultra-free", object: "model" },
      { id: "opencode/north-mini-code-free", object: "model" },
      { id: "opencode/laguna-s-2.1-free", object: "model" },
      { id: "opencode/big-pickle", object: "model" },
      { id: "opencode/ling-3.0-flash-free", object: "model" },
    ],
  });
}
app.get("/v1/models", handleModels);
app.get("/models", handleModels);

// =====================================================
// ENDPOINT 1: OpenAI format (for HERMES)
// =====================================================
async function handleChat(req, res) {
  const { model, messages, stream, tools, tool_choice, max_tokens, temperature, top_p, stop } = req.body;
  const isStreaming = stream === true;
  const zenModel = (model || "deepseek-v4-flash-free").replace("opencode/", "");

  const zenBody = { model: zenModel, messages: messages || [], stream: isStreaming };
  if (tools && tools.length > 0) zenBody.tools = tools;
  if (tool_choice) zenBody.tool_choice = tool_choice;
  if (max_tokens) zenBody.max_tokens = max_tokens;
  if (temperature !== undefined) zenBody.temperature = temperature;
  if (top_p !== undefined) zenBody.top_p = top_p;
  if (stop) zenBody.stop = stop;

  // Debug: Log full details for vision requests
  let hasImage = false;
  let imageSize = 0;
  let payloadSize = JSON.stringify(zenBody).length;
  if (messages) {
    for (const msg of messages) {
      if (Array.isArray(msg.content)) {
        for (const block of msg.content) {
          if (block.type === "image_url") {
            hasImage = true;
            imageSize = block.image_url?.url?.length || 0;
          }
        }
      }
    }
  }
  console.log(`[HERMES] ${zenModel} | stream=${isStreaming} | msgs=${messages?.length || 0} | tools=${tools?.length || 0} | payload=${(payloadSize/1024).toFixed(1)}KB | image=${hasImage} | imgSize=${(imageSize/1024).toFixed(1)}KB`);

  try {
    const zenRes = await fetch(`${ZEN_BASE}/chat/completions`, {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "User-Agent": "OpenCode/1.17.8 (windows; x64)",
        "x-opencode-version": "1.17.8",
        "x-opencode-session": "hermes-bridge-fixed"
      },
      body: JSON.stringify(zenBody),
    });
    if (!zenRes.ok) {
      const errText = await zenRes.text();
      console.log(`[BRIDGE-ERROR] ${zenModel} | HTTP ${zenRes.status} | image=${hasImage} | error=${errText.substring(0, 300)}`);
      res.status(zenRes.status).json({ error: { message: errText } });
      return;
    }
    if (isStreaming) {
      res.setHeader("Content-Type", "text/event-stream");
      res.setHeader("Cache-Control", "no-cache");
      res.setHeader("Connection", "keep-alive");
      res.flushHeaders();
      const decoder = new TextDecoder();
      for await (const chunk of zenRes.body) {
        const text = decoder.decode(chunk, { stream: true });
        const fixed = text.replaceAll(`"model":"${zenModel}"`, `"model":"${model}"`);
        res.write(fixed);
      }
      res.end();
    } else {
      const data = await zenRes.json();
      if (data.model) data.model = model;
      res.json(data);
    }
  } catch (err) {
    res.status(500).json({ error: { message: err.message } });
  }
}
app.post("/v1/chat/completions", handleChat);
app.post("/chat/completions", handleChat);

// =====================================================
// ENDPOINT 2: Web Search (DuckDuckGo)
// =====================================================
app.post("/v1/web/search", async (req, res) => {
  const { query, action, url } = req.body;
  if (!query && !url) return res.status(400).json({ error: "query or url required" });

  try {
    // Open a page and return its content
    if (action === "open_page" && url) {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 30000);
      try {
        const resp = await fetch(url, {
          signal: controller.signal,
          headers: { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" },
        });
        clearTimeout(timeout);
        const html = await resp.text();
        if (html.length > 5242880) return res.status(413).json({ error: "content too large" });

        // HTML → Text with htmlparser2
        let textParts = [];
        const parser = new htmlparser2.Parser({
          ontext(text) { textParts.push(text); },
          onclosetag(name) { if (name === "p" || name === "br" || name === "li" || name === "h1" || name === "h2" || name === "h3" || name === "h4") textParts.push("\n"); },
        });
        parser.write(html);
        parser.end();
        const plainText = textParts.join("").replace(/\n{3,}/g, "\n\n").trim();

        // Also make markdown via turndown
        const markdown = turndown.turndown(html).substring(0, 500000);

        res.json({
          url,
          contentType: resp.headers.get("content-type") || "text/html",
          format: "markdown",
          output: markdown,
          text: plainText.substring(0, 500000),
        });
      } catch (e) {
        clearTimeout(timeout);
        throw e;
      }
    } else {
      // DuckDuckGo Lite search
      const searchQuery = query || "";
      const searchUrl = `https://lite.duckduckgo.com/lite/?q=${encodeURIComponent(searchQuery)}`;
      const resp = await fetch(searchUrl, {
        headers: { "User-Agent": "Mozilla/5.0" },
      });
      const html = await resp.text();

      // Parse HTML results
      const results = [];
      let currentResult = null;
      let inResult = false;
      let linkCount = 0;

      const parser = new htmlparser2.Parser({
        onopentag(name, attribs) {
          if (name === "a" && attribs.href && attribs.href !== "#" && !attribs.href.startsWith("//")) {
            if (linkCount > 0 && !inResult) {
              currentResult = { url: attribs.href, title: "", snippet: "" };
              inResult = true;
            }
            linkCount++;
          }
        },
        ontext(text) {
          if (inResult && currentResult) {
            const trimmed = text.trim();
            if (trimmed) {
              if (!currentResult.title) currentResult.title = trimmed;
              else if (trimmed.length > 20) currentResult.snippet = trimmed;
            }
          }
        },
        onclosetag(name) {
          if (name === "a" && inResult && currentResult) {
            results.push(currentResult);
            currentResult = null;
            inResult = false;
          }
        },
      });
      parser.write(html);
      parser.end();

      res.json({
        query: searchQuery,
        results: results.slice(0, 10),
      });
    }
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// =====================================================
// ENDPOINT 3: Web Fetch
// =====================================================
app.post("/v1/web/fetch", async (req, res) => {
  const { url, format } = req.body;
  if (!url) return res.status(400).json({ error: "url is required" });

  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000);
    const resp = await fetch(url, {
      signal: controller.signal,
      headers: { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" },
    });
    clearTimeout(timeout);
    const html = await resp.text();
    if (html.length > 5242880) return res.status(413).json({ error: "content too large" });

    if (format === "html") {
      res.json({ url, contentType: resp.headers.get("content-type") || "text/html", format: "html", output: html.substring(0, 500000) });
    } else if (format === "text") {
      let textParts = [];
      const parser = new htmlparser2.Parser({
        ontext(text) { textParts.push(text); },
        onclosetag(name) { if (name === "p" || name === "br" || name === "li" || name === "h1" || name === "h2" || name === "h3" || name === "h4") textParts.push("\n"); },
      });
      parser.write(html);
      parser.end();
      const plainText = textParts.join("").replace(/\n{3,}/g, "\n\n").trim();
      res.json({ url, contentType: resp.headers.get("content-type") || "text/html", format: "text", output: plainText.substring(0, 500000) });
    } else {
      // Default: markdown
      const markdown = turndown.turndown(html).substring(0, 500000);
      res.json({ url, contentType: resp.headers.get("content-type") || "text/html", format: "markdown", output: markdown });
    }
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PROXY_PORT, "127.0.0.1", () => {
  console.log(`[BRIDGE] Running at http://127.0.0.1:${PROXY_PORT}`);
  console.log(`[BRIDGE] Hermes  -> /v1/chat/completions (OpenAI format)`);
  console.log(`[BRIDGE] Web     -> /v1/web/search + /v1/web/fetch`);
  console.log(`[BRIDGE] Backend -> ${ZEN_BASE} (OpenCode Free Models)`);
});
