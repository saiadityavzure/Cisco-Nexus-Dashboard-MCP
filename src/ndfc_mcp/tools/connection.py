"""Tools: Connection & General.

test_connection, test_switch_connectivity, serve_dashboard,
get_active_tools, raw_query, ai_chat
"""

import logging

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolError

from ..types import ResourceDict, ResourceList
from .dependencies import get_ndfc_client_dep

logger = logging.getLogger(__name__)


def register_tools(mcp: FastMCP) -> None:

    @mcp.tool(annotations={"title": "Test NDFC Connection", "readOnlyHint": True})
    async def test_connection() -> ResourceDict:
        """Test connectivity to the Nexus Dashboard Fabric Controller (NDFC) and return version info."""
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Test Switch Connectivity", "readOnlyHint": True})
    async def test_switch_connectivity(serial_number: str) -> ResourceDict:
        """Test reachability to a specific switch managed by NDFC.

        Args:
            serial_number: Switch serial number or hostname.
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Get Active Tool Groups", "readOnlyHint": True})
    async def get_active_tools() -> ResourceList:
        """Return the list of currently enabled MCP tool groups."""
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Raw NDFC API Query", "readOnlyHint": True})
    async def raw_query(endpoint: str, method: str = "GET", body: dict | None = None) -> ResourceDict:
        """Pass a raw HTTP request through to the NDFC API.

        Use this as an escape hatch when no dedicated tool covers the endpoint.

        Args:
            endpoint: API path (e.g. /appcenter/cisco/ndfc/api/v1/...).
            method: HTTP method — GET, POST, PUT, PATCH, DELETE.
            body: Request body for POST/PUT/PATCH.
        """
        # TODO: implement
        raise NotImplementedError
