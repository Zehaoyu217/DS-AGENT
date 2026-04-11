# Ollama Integration for claude-code-agent

Runs claude-code-agent against local Ollama models via a LiteLLM proxy that translates Anthropic API ↔ Ollama.

## Quick Start

```bash
# From the claude-code-agent root:
source ollama/start.sh                  # default: qwen3.5:9b
source ollama/start.sh gemma4:31b       # or any Ollama model you have

# Once the proxy is ready:
bun run start
```

## Available Models (currently installed)

| Model | Best for |
|-------|---------|
| `qwen3.5:9b` | Fast iteration, tool use, coding |
| `gemma4:e4b` | Small, embedded tasks |
| `gemma4:31b` | Complex reasoning |
| `gemma2:27b-instruct-q6_K` | Balanced quality |

## How It Works

```
claude-code-agent (@anthropic-ai/sdk)
        ↓
ANTHROPIC_BASE_URL=http://localhost:4000
        ↓
LiteLLM proxy (litellm.yaml)
        ↓
Ollama (http://localhost:11434)
        ↓
Local model (e.g. qwen3.5:9b)
```

The Anthropic SDK reads `ANTHROPIC_BASE_URL` automatically. LiteLLM translates
Anthropic Messages API format → OpenAI format → Ollama.

## Env Vars (set by start.sh)

| Variable | Value |
|----------|-------|
| `ANTHROPIC_BASE_URL` | `http://localhost:4000` |
| `ANTHROPIC_API_KEY` | `sk-ollama-local` (dummy) |
| `ANTHROPIC_MODEL` | chosen model |
| `ANTHROPIC_SMALL_FAST_MODEL` | chosen model (reuses same for fast tasks) |

## Stop

```bash
bash ollama/stop.sh
```
