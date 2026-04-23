import logging

from mcp.server.fastmcp import FastMCP

from .settings import settings
from .tools import (
    connection,
    execution,
    fabrics,
    interfaces,
    networks,
    switches,
    troubleshooting,
    vrfs,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Newer FastMCP versions accept description.
    mcp = FastMCP(
        name="ndfc-mcp",
        description="MCP server for Cisco Nexus Dashboard Fabric Controller (NDFC)",
    )
except TypeError:
    # Older FastMCP versions accept only name.
    mcp = FastMCP(name="ndfc-mcp")

# Register all tool groups
connection.register_tools(mcp)
fabrics.register_tools(mcp)
switches.register_tools(mcp)
vrfs.register_tools(mcp)
networks.register_tools(mcp)
interfaces.register_tools(mcp)

if settings.enable_execution_tools:
    execution.register_tools(mcp)

if settings.enable_troubleshooting_tools:
    troubleshooting.register_tools(mcp)

# ASGI app exposed for uvicorn (SSE / HTTP transport)
app = mcp.sse_app()

if __name__ == "__main__":
    # stdio mode
    mcp.run(transport="stdio")
