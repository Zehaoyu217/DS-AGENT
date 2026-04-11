#!/bin/bash
# Stop the LiteLLM proxy started by start.sh
if [ -f /tmp/litellm-ollama.pid ]; then
  PID=$(cat /tmp/litellm-ollama.pid)
  kill $PID 2>/dev/null && echo "Stopped LiteLLM proxy (PID $PID)" || echo "Already stopped"
  rm -f /tmp/litellm-ollama.pid
else
  # Fallback: kill by port
  lsof -ti:4000 | xargs kill -9 2>/dev/null && echo "Stopped proxy on port 4000" || echo "Nothing running on port 4000"
fi
