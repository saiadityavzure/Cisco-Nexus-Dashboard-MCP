#!/usr/bin/env bash
set -euo pipefail

TRANSPORT="${TRANSPORT:-sse}"

if [ "$TRANSPORT" = "stdio" ]; then
    exec python -m ndfc_mcp.server
else
    # Both "sse" and "http" run via uvicorn — FastMCP exposes the right ASGI app
    exec uvicorn ndfc_mcp.server:app \
        --host "${HOST:-0.0.0.0}" \
        --port "${PORT:-8000}"
fi
