#!/usr/bin/env bash
set -euo pipefail

echo "=== Analytical Agent — Local Development ==="
echo ""

# Check prerequisites
command -v python3 >/dev/null 2>&1 || { echo "Python 3 required"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "Node.js required"; exit 1; }

# Backend
if [ ! -d "backend/.venv" ]; then
    echo "Setting up backend virtualenv..."
    cd backend && python3 -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]" && cd ..
else
    source backend/.venv/bin/activate
fi

# Frontend
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing frontend dependencies..."
    cd frontend && npm install && cd ..
fi

echo ""
echo "Starting services..."
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:5173"
echo "  Health:   http://localhost:8000/api/health"
echo ""

make dev
