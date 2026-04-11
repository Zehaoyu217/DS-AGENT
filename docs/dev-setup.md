# Development Setup

## Prerequisites

- Python 3.12+
- Node.js 20+ (for frontend)
- Docker + Docker Compose (for local services)
- Ollama (for local models)

## Quick Start

```bash
# 1. Clone and enter
git clone https://github.com/Zehaoyu217/analytical-agent.git
cd analytical-agent

# 2. Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cd ..

# 3. Frontend
cd frontend
npm install
cd ..

# 4. Environment
cp .env.example .env
# Edit .env with your settings

# 5. Start everything
make dev
```

## Individual Services

```bash
make backend          # Backend only (uvicorn on :8000)
make frontend         # Frontend only (vite on :5173)
```

## Running Tests

```bash
make test             # All tests
make test-backend     # Backend only (pytest)
make test-frontend    # Frontend only (vitest)
```

## Ollama Setup

```bash
# Install Ollama: https://ollama.ai
ollama pull qwen3.5:9b
source infra/ollama/start.sh
```
