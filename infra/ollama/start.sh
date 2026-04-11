#!/bin/bash
# Start claude-code-agent with Ollama via LiteLLM proxy
# Usage: source ollama/start.sh [model]
#   model defaults to qwen3.5:9b

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODEL="${1:-qwen3.5:9b}"
LITELLM_PORT=4000
LITELLM_BASE_URL="http://localhost:${LITELLM_PORT}"

# ── 1. Check Ollama is running ───────────────────────────────────────────────
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
  echo "ERROR: Ollama is not running. Start it with: ollama serve"
  exit 1
fi

# ── 2. Check model exists in Ollama ─────────────────────────────────────────
if ! curl -s http://localhost:11434/api/tags | python3 -c "
import sys, json
models = [m['name'] for m in json.load(sys.stdin)['models']]
model = '${MODEL}'
if model not in models:
    print(f'ERROR: Model \"{model}\" not found in Ollama.')
    print(f'Available: {chr(10).join(models)}')
    print(f'Pull with: ollama pull {model}')
    sys.exit(1)
print(f'✓ Model {model} found')
"; then
  exit 1
fi

# ── 3. Install litellm if needed ─────────────────────────────────────────────
if ! command -v litellm &> /dev/null; then
  echo "Installing litellm..."
  pip install litellm[proxy] -q
fi

# ── 4. Kill any existing litellm proxy on this port ──────────────────────────
if lsof -ti:${LITELLM_PORT} > /dev/null 2>&1; then
  echo "Stopping existing proxy on port ${LITELLM_PORT}..."
  lsof -ti:${LITELLM_PORT} | xargs kill -9 2>/dev/null || true
  sleep 1
fi

# ── 5. Start LiteLLM proxy in background ─────────────────────────────────────
echo "Starting LiteLLM proxy on port ${LITELLM_PORT}..."
litellm --config "${SCRIPT_DIR}/litellm.yaml" --port ${LITELLM_PORT} \
  --log_level ERROR > /tmp/litellm-ollama.log 2>&1 &
LITELLM_PID=$!

# Wait for proxy to be ready
for i in {1..20}; do
  if curl -s "${LITELLM_BASE_URL}/health" > /dev/null 2>&1; then
    echo "✓ LiteLLM proxy ready"
    break
  fi
  sleep 0.5
done

if ! curl -s "${LITELLM_BASE_URL}/health" > /dev/null 2>&1; then
  echo "ERROR: LiteLLM proxy failed to start. Check /tmp/litellm-ollama.log"
  exit 1
fi

# ── 6. Export env vars for claude-code-agent ─────────────────────────────────
export ANTHROPIC_BASE_URL="${LITELLM_BASE_URL}"
export ANTHROPIC_API_KEY="sk-ollama-local"
export ANTHROPIC_MODEL="${MODEL}"
export ANTHROPIC_SMALL_FAST_MODEL="${MODEL}"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  claude-code-agent → Ollama"
echo "  Model:  ${MODEL}"
echo "  Proxy:  ${LITELLM_BASE_URL}"
echo "  PID:    ${LITELLM_PID}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Run 'bun run start' to launch the agent"
echo "To stop proxy: kill ${LITELLM_PID}"
echo ""

# Save PID for cleanup
echo $LITELLM_PID > /tmp/litellm-ollama.pid
