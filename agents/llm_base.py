#!/usr/bin/env python3
"""HermesZen ADK — Base LLM Connection (DeepSeek via OpenCode Zen bridge)

VERIFIED on hermeszen-adk-vm (2026-08-16): returns "HELLO" from DeepSeek.

Dependencies:
  pip install google-adk "litellm>=1.84" "pydantic>=2.12.5"

KNOWN FIX (litellm 1.90/1.97 bug): missing import in litellm/types/utils.py
  add:  ChatCompletionReasoningSummaryTextBlock,
  after: ChatCompletionRedactedThinkingBlock,
  (class is defined in litellm/types/llms/openai.py but not imported)
"""
import litellm
from litellm.types.utils import Message
Message.model_rebuild(force=True)

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import InMemoryRunner
from google.genai import types

BRIDGE_URL = "http://127.0.0.1:4000/v1"
BRIDGE_KEY = "local-master-key"
CHAT_MODEL = "opencode/deepseek-v4-flash-free"


def build_model(model_name: str = CHAT_MODEL) -> LiteLlm:
    """Create a LiteLlm connector pointing at the local bridge."""
    return LiteLlm(
        model=f"openai/{model_name}",
        api_base=BRIDGE_URL,
        api_key=BRIDGE_KEY,
    )


def run_agent(agent: LlmAgent, message: str, session_id: str = "s1") -> str:
    """Run an ADK agent with auto-created in-memory session, return final text."""
    runner = InMemoryRunner(agent=agent, app_name="hermeszen-adk")
    runner.session_service.create_session_sync(
        app_name="hermeszen-adk", user_id="user1", session_id=session_id)
    content = types.Content(role="user",
                            parts=[types.Part.from_text(text=message)])
    for event in runner.run(user_id="user1", session_id=session_id,
                            new_message=content):
        if event.is_final_response():
            return str(event.content)
    return "(no reply)"


def main():
    model = build_model()
    agent = LlmAgent(
        name="hello_agent",
        model=model,
        instruction="You are a helpful assistant. Answer briefly.",
    )
    print("AGENT_BUILT OK | model:", type(model).__name__)
    print("CALLING DeepSeek via bridge...")
    reply = run_agent(agent, "Say HELLO in one word")
    print("REPLY:", reply)
    print("TEST_DONE")


if __name__ == "__main__":
    main()