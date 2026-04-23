# Nexus Dashboard Fabric Controller MCP Server

MCP server for Cisco Nexus Dashboard Fabric Controller (NDFC). The project exposes NDFC operations as Model Context Protocol tools so an MCP client can inspect fabrics, topology, inventory, compliance state, and eventually manage switches, VRFs, networks, interfaces, execution, and troubleshooting workflows.

This repository is currently in active development. The fabric tools are the first implemented tool group; the remaining tool modules are scaffolded and registered so their API shape can evolve as the implementation is completed.

## Current Status

Implemented:

- Fabric listing, creation, deletion, summary, detail, topology, inventory, compliance, config save, config deploy, recalculate/deploy, and config preview.
- Shared async NDFC REST client using `httpx`.
- Environment-based settings via `pydantic-settings`.
- MCP stdio transport for local client integrations.
- SSE/HTTP transport through FastMCP's ASGI app and Uvicorn.
- Docker and Docker Compose scaffolding.

Scaffolded but not yet implemented:

- Connection tools: connectivity checks, active tool discovery, raw query.
- Switch tools: switch listing/detail, policies, freeform config, rediscovery, maintenance mode, templates.
- VRF tools: list/create/attach/detach/deploy/delete.
- Network tools: list/create/attach/detach/deploy/delete.
- Interface tools: list/provision/deploy.
- Execution tools: NX-API and SSH execution.
- Troubleshooting tools: guided diagnostics, alarms, events, read-only NX-API diagnostics.

## Project Layout

```text
src/ndfc_mcp/
  server.py                 FastMCP server and tool registration
  settings.py               Environment-driven configuration
  ndfc_client.py            Thin async HTTP client for NDFC REST calls
  types.py                  Shared simple output aliases
  tools/
    connection.py           General/connection tool group
    dependencies.py         Shared client, resolver, and heartbeat helpers
    fabrics.py              Fabric management tools
    switches.py             Switch management tools
    vrfs.py                 VRF management tools
    networks.py             Network management tools
    interfaces.py           Interface management tools
    execution.py            NX-API/SSH execution tools
    troubleshooting.py      Troubleshooting tools
  ndfc/schemas/             Pydantic models for NDFC request/response shapes
```

## Requirements

- Python 3.11 or newer
- Access to a Cisco Nexus Dashboard / NDFC instance
- NDFC API token, or credentials if password fallback is later implemented

Python dependencies are defined in `pyproject.toml`:

- `fastmcp`
- `httpx`
- `pydantic`
- `pydantic-settings`
- `asyncssh`
- `uvicorn`

## Configuration

Create a `.env` file in the project root:

```env
NDFC_HOST=https://ndfc.example.com
NDFC_USERNAME=admin
NDFC_API_KEY=your-api-token
NDFC_VERIFY_SSL=false

TRANSPORT=stdio
HOST=0.0.0.0
PORT=8000

ENABLE_EXECUTION_TOOLS=true
ENABLE_TROUBLESHOOTING_TOOLS=true
ENABLE_WRITE_TOOLS=true

SSH_USERNAME=
SSH_PASSWORD=
SSH_TIMEOUT=30

NXAPI_PORT=443
NXAPI_VERIFY_SSL=false
```

Notes:

- `NDFC_HOST` should be the Nexus Dashboard base URL, for example `https://10.0.0.10`.
- The client prepends `/api` to short endpoints internally.
- `NDFC_API_KEY` is sent as the `X-Auth-Token` header.
- `NDFC_VERIFY_SSL=false` is useful for lab systems with self-signed certificates. Use `true` when a trusted certificate chain is available.

## Run Locally

Install the project in editable mode:

```powershell
python -m pip install -e .
```

Run in stdio mode:

```powershell
python -m ndfc_mcp.server
```

Run the HTTP/SSE app with Uvicorn:

```powershell
uvicorn ndfc_mcp.server:app --host 0.0.0.0 --port 8000
```

## Run With Docker

Build and start the service:

```powershell
docker compose up --build
```

The compose file sets:

```env
TRANSPORT=http
HOST=0.0.0.0
PORT=8000
```

and publishes the server on port `8000`.

## MCP Client Configuration

For a local stdio MCP client, point the client at the Python module:

```json
{
  "mcpServers": {
    "ndfc-mcp": {
      "command": "python",
      "args": ["-m", "ndfc_mcp.server"],
      "env": {
        "NDFC_HOST": "https://ndfc.example.com",
        "NDFC_USERNAME": "admin",
        "NDFC_API_KEY": "your-api-token",
        "NDFC_VERIFY_SSL": "false"
      }
    }
  }
}
```

For HTTP/SSE clients, run the Uvicorn app and configure the client with the server URL exposed by FastMCP.

## Implemented Fabric Tools

The following tools are implemented in `src/ndfc_mcp/tools/fabrics.py`:

- `get_fabrics`
- `create_fabric`
- `delete_fabric`
- `get_fabric_summary`
- `get_fabric_detail`
- `get_topology`
- `get_full_topology`
- `get_fabric_inventory`
- `get_compliance`
- `config_save`
- `config_deploy`
- `recalculate_and_deploy`
- `config_preview`

Long-running deploy operations use the shared heartbeat wrapper so SSE clients can keep the request alive while NDFC completes the operation.

## Development Notes

Tool modules follow the same pattern:

1. Import `FastMCP`, `ToolError`, shared return types, and helpers from `tools.dependencies`.
2. Define a `register_tools(mcp: FastMCP) -> None` function.
3. Register each tool with `@mcp.tool(...)`.
4. Resolve human-friendly names to canonical NDFC identifiers before calling the API.
5. Catch `httpx.HTTPStatusError` and raise `ToolError` with the HTTP status and response body.
6. Return simple dictionaries/lists that are easy for an LLM to read instead of raw, deeply nested API responses where possible.

When adding a new tool, prefer adding any reusable validation, resolver, or long-running-operation behavior to `tools/dependencies.py` rather than duplicating it across tool modules.

## Safety

Several tool groups will eventually perform write or execution operations against network infrastructure. Keep these guardrails in mind while implementing:

- Validate required arguments before sending requests to NDFC.
- Resolve fabric, switch, VRF, and network names to canonical values where possible.
- Keep read-only tools annotated with `readOnlyHint`.
- Respect `ENABLE_WRITE_TOOLS` before exposing destructive or mutating actions.
- Keep execution tools behind `ENABLE_EXECUTION_TOOLS`.
- Prefer explicit, narrow tool arguments over raw payload pass-throughs.

## Roadmap

Near-term implementation targets:

- Finish `connection.py` with connection testing, active tool reporting, and a guarded `raw_query`.
- Implement switch inventory/detail/policy workflows.
- Implement VRF and network lifecycle operations.
- Add interface provisioning and deployment.
- Implement NX-API/SSH execution with clear safety boundaries.
- Add focused tests for resolvers, request payload construction, and error translation.
