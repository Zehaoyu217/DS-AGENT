#!/usr/bin/env bash
# Wrapper for `make graphify` — runs the graphify pipeline against the project
# root and copies output into the canonical knowledge/graphs/ + graphify/
# locations.
#
# Usage:
#   bash scripts/run_graphify.sh                 # full pipeline, default scope
#   bash scripts/run_graphify.sh --update        # incremental — re-extract changed files only
#   bash scripts/run_graphify.sh --cluster-only  # rerun clustering on existing graph
#   bash scripts/run_graphify.sh --no-viz        # skip HTML viz
#   bash scripts/run_graphify.sh <path>          # graphify a specific subdirectory
#
# This is a deterministic CLI wrapper, NOT a re-run of the LLM extraction pipeline.
# To rebuild the graph from scratch with semantic extraction, invoke the /graphify
# slash command from Claude Code instead.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

OUT_DIR="${REPO_ROOT}/graphify-out"
PUBLISH_DIR="${REPO_ROOT}/graphify"
KNOWLEDGE_DIR="${REPO_ROOT}/knowledge/graphs"

# Detect graphify executable
if command -v graphify >/dev/null 2>&1; then
    GRAPHIFY_BIN="graphify"
else
    echo "ERROR: graphify not installed."
    echo ""
    echo "Install it with:  pip install graphifyy"
    echo ""
    echo "Or invoke the /graphify slash command from Claude Code, which"
    echo "auto-installs and runs the full LLM extraction pipeline."
    exit 1
fi

ARGS=("$@")

# Default to current dir if no path-like first arg is supplied
if [ "${#ARGS[@]}" -eq 0 ] || [[ "${ARGS[0]}" == --* ]]; then
    SCOPE_ARG=()
else
    SCOPE_ARG=("${ARGS[0]}")
    ARGS=("${ARGS[@]:1}")
fi

mkdir -p "$OUT_DIR" "$PUBLISH_DIR" "$KNOWLEDGE_DIR"

echo "==> running graphify against ${SCOPE_ARG[*]:-.}"
"$GRAPHIFY_BIN" "${SCOPE_ARG[@]}" "${ARGS[@]}"

if [ -d "$OUT_DIR" ] && [ "$(ls -A "$OUT_DIR" 2>/dev/null)" ]; then
    echo "==> publishing artifacts to $PUBLISH_DIR/"
    cp -R "$OUT_DIR"/. "$PUBLISH_DIR"/
    echo "==> publishing graph + manifest to $KNOWLEDGE_DIR/"
    for f in graph.json graph.html GRAPH_REPORT.md manifest.json; do
        if [ -f "$OUT_DIR/$f" ]; then
            cp "$OUT_DIR/$f" "$KNOWLEDGE_DIR/$f"
        fi
    done
    echo "done. Published files:"
    ls -1 "$PUBLISH_DIR" | sed 's/^/  /'
else
    echo "WARNING: $OUT_DIR is empty — graphify produced no output."
    exit 1
fi
