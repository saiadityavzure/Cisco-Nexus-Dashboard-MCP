#!/usr/bin/env bash
set -euo pipefail

TRANSPORT="${TRANSPORT:-sse}"

# Ensure src-layout package imports resolve in both image-only and bind-mount runs.
export PYTHONPATH="${PYTHONPATH:+${PYTHONPATH}:}/app/src"

if [ "$TRANSPORT" = "stdio" ]; then
    exec python -m ndfc_mcp.server
else
    # Both "sse" and "http" run via uvicorn — FastMCP exposes the right ASGI app
    exec uvicorn ndfc_mcp.server:app \
        --app-dir /app/src \
        --host "${HOST:-0.0.0.0}" \
        --port "${PORT:-8000}"
fi
