# 🤖 HermesZen ADK — AI Agent Team That Builds Daily

<div align="center">

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Google ADK](https://img.shields.io/badge/Google-ADK_2.7-red.svg)](https://github.com/google/adk-python)
[![DeepSeek](https://img.shields.io/badge/LLM-DeepSeek_V4_Flash-yellow.svg)](https://opencode.ai/zen)
[![OpenCode Zen](https://img.shields.io/badge/Backend-OpenCode_Zen_Free-brightgreen.svg)](https://opencode.ai/zen)
[![GCP](https://img.shields.io/badge/Cloud-GCP_Free_Tier-orange.svg)](https://cloud.google.com)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](#)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%2F%20Windows-brightgreen.svg)](#)
[![GitHub](https://img.shields.io/badge/GitHub-Automation-black.svg)](#)

*A multi-agent developer team powered by Google ADK — builds real projects, contributes to trending repos, and maintains a living GitHub portfolio — all on a free GCP VM with free AI models.*

</div>

---

## ✨ What Is This?

This is a **self-running AI developer team** that works like real developers:

- 🤖 **8 specialist agents** (Scout, Planner, Coder, Reviewer, Security, README, Git, Telegram)
- 🧠 Powered by **Google ADK** (Agent Development Kit) + **DeepSeek V4 Flash** (free, via OpenCode Zen)
- 🌉 All AI calls flow through a **local bridge** (fixed-session, rate-limit safe)
- 📱 **Telegram control** — tell it what to build, get updates on every step
- 🐙 Everything lands on **GitHub** — real commits, PRs, and a growing portfolio

**The mission:** daily real work — new projects, open-source contributions, security checks, professional READMEs — so the portfolio writes itself while you learn.

---

## 🏗️ Architecture

```
📱 TELEGRAM (your control center)
      │
      ▼
🤖 HERMES (orchestrator — Telegram connected)
      │
      ▼
🧩 ADK AGENT TEAM (8 specialists + tools)
   ├── 🕵️ Scout      → finds trending repos / good-first-issues
   ├── 👨‍💼 Planner    → picks today's best task
   ├── 👨‍💻 Coder     → writes code / contributions
   ├── 🧪 Reviewer   → quality check (max 2 retries)
   ├── 🛡️ Security   → secret & dependency audit
   ├── 📝 README     → professional docs & badges
   ├── 🚀 Git        → commit / push / PR
   └── 📱 Telegram   → step-by-step updates
      │
      ▼
🌉 BRIDGE (127.0.0.1:4000) — OpenCode Zen proxy (fixed session)
      │
      ▼
⚡ DeepSeek V4 Flash (+ MiMo for vision) — 100% FREE
```

---

## 📅 Weekly Task Rotation

| Day | Task Type | Example |
|-----|-----------|---------|
| Mon | New project | weather-cli, todo-api, quiz-game |
| Tue | Trending repo contribution | popular repo good-first-issue PR |
| Wed | New project (medium) | scraper, csv analyzer |
| Thu | Professional README (PR) | upgrade a repo's docs |
| Fri | Security check + fix | secret scan + dependency audit |
| Sat | Showcase project | dashboard, telegram bot |
| Sun | Rest / backlog | catch up, polish |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- GCP free-tier VM (e2-micro) — or any Linux machine
- Telegram Bot token (BotFather)

### Setup

```bash
# 1. Clone
git clone https://github.com/yousufkidiya17/hermeszen-adk.git
cd hermeszen-adk

# 2. Bridge (LLM access via OpenCode Zen free models)
cd bridge && npm install && node server.mjs &
# → http://127.0.0.1:4000/v1 (DeepSeek + MiMo)

# 3. ADK agents
cd ..
python3 -m pip install google-adk "litellm>=1.84"

# 4. GitHub access
# Add your SSH deploy key to this repo (Settings → Deploy keys)

# 5. Run the team
python3 workflow.py
```

### Test the pipeline

```bash
# Verify bridge → DeepSeek
curl http://127.0.0.1:4000/v1/models

# Run one agent standalone
python3 agents/planner.py --test
```

---

## 📁 Project Structure

```
hermeszen-adk/
├── bridge/
│   ├── server.mjs          # fixed bridge (DeepSeek via OpenCode Zen)
│   └── package.json
├── agents/
│   ├── scout.py            # trending repos / good-first-issues
│   ├── planner.py          # task selection + plan
│   ├── coder.py            # code + contributions
│   ├── reviewer.py         # quality gate
│   ├── security.py         # secret & dependency audit
│   ├── readme.py           # professional READMEs
│   ├── git.py              # commit / push / PR
│   └── telegram.py         # daily reports
├── workflow.py             # ADK graph (8 agents)
├── tools/
│   ├── github_tool.py      # repo/issue/PR helpers
│   └── security_tool.py    # scan helpers
├── idea_pool.md            # 100+ project ideas
├── config.yaml             # LiteLLM bridge config
├── run_daily.sh            # cron entry point
├── work/                   # daily output (committed)
└── README.md               # this file
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent framework | **Google ADK 2.7** (LiteLLM connector) |
| LLM | **DeepSeek V4 Flash** (free) + **MiMo V2.5** (vision, free) |
| Model gateway | OpenCode Zen via local bridge (fixed session, UA spoof) |
| Orchestration | Hermes Agent (Telegram + workflow control) |
| Cloud | GCP free tier (e2-micro, 100GB) |
| Version control | GitHub (deploy key, SSH) |
| Notifications | Telegram Bot API |

---

## 🔒 Security

- 🛡️ Dedicated **Security Agent** — scans for secrets, unsafe patterns, vulnerable deps
- 🔑 GitHub via **deploy key** (repo-scoped, no broad access)
- 🌉 Bridge binds to localhost only
- ✅ Reviewer gate before every commit

---

## 🤝 Contributing

Contributions are welcome! This repo is itself built by AI agents — feel free to open issues, suggest tasks, or fork it for your own portfolio.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push + open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ by [Yousuf Kidiya](https://github.com/yousufkidiya17) + AI Agent Team**

![Stars](https://img.shields.io/github/stars/yousufkidiya17/hermeszen-adk?style=social)
![Forks](https://img.shields.io/github/forks/yousufkidiya17/hermeszen-adk?style=social)

</div>
