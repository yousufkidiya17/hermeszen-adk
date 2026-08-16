#!/bin/bash
# HermesZen ADK — VM setup script (verified on hermeszen-adk-vm 2026-08-16)
set -e

echo "=== [1/4] System packages ==="
sudo apt-get update -qq
sudo apt-get install -y -qq python3 python3-pip python3-venv nodejs npm git curl

echo "=== [2/4] Bridge deps ==="
cd "$(dirname "$0")/bridge"
npm install

echo "=== [3/4] ADK + LiteLLM ==="
pip install -r requirements.txt

echo "=== [4/4] Patch litellm bug (missing import) ==="
python3 - <<'PYEOF'
import litellm, os
p = os.path.join(os.path.dirname(litellm.__file__), "types", "utils.py")
src = open(p).read()
if "ChatCompletionReasoningSummaryTextBlock," not in src:
    src = src.replace(
        "ChatCompletionRedactedThinkingBlock,",
        "ChatCompletionRedactedThinkingBlock,\n    ChatCompletionReasoningSummaryTextBlock,",
    )
    open(p, "w").write(src)
    print("PATCHED litellm types/utils.py")
else:
    print("litellm patch already applied")
PYEOF

echo "=== DONE. Next: node bridge/server.mjs & python3 agents/llm_base.py ==="