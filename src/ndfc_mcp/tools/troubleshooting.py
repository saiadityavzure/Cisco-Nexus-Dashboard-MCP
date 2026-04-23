"""Tools: Troubleshooting.

troubleshoot_wizard, troubleshoot_summary, run_nxapi, get_alarms, get_events
"""

import logging

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolError

from ..types import ResourceDict, ResourceList
from .dependencies import get_ndfc_client_dep

logger = logging.getLogger(__name__)


def register_tools(mcp: FastMCP) -> None:

    @mcp.tool(annotations={"title": "Troubleshoot Wizard", "readOnlyHint": True})
    async def troubleshoot_wizard(fabric_name: str, issue_description: str) -> ResourceDict:
        """Launch an interactive troubleshooting flow for a fabric issue.

        Runs a series of diagnostics (compliance check, alarm scan, connectivity tests)
        and returns a structured summary with recommended actions.

        Args:
            fabric_name: Name of the fabric to troubleshoot.
            issue_description: Free-text description of the problem being investigated.
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Get Troubleshoot Summary", "readOnlyHint": True})
    async def troubleshoot_summary(fabric_name: str) -> ResourceDict:
        """Get a quick health summary for a fabric (alarms, compliance errors, unreachable switches).

        Args:
            fabric_name: Name of the fabric.
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Run NX-API (Troubleshoot)", "readOnlyHint": True})
    async def run_nxapi(host: str, command: str) -> ResourceDict:
        """Run an NX-API show command as part of a troubleshooting flow.

        This is a read-only variant of nxapi_exec intended for diagnostic use.

        Args:
            host: Switch IP address or hostname.
            command: Show command to run (e.g. "show bgp summary").
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Get NDFC Alarms", "readOnlyHint": True})
    async def get_alarms(fabric_name: str = "", severity: str = "") -> ResourceList:
        """Retrieve active alarms from NDFC.

        Args:
            fabric_name: Filter alarms to a specific fabric (empty = all fabrics).
            severity: Filter by severity — CRITICAL, MAJOR, MINOR, WARNING (empty = all).
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Get NDFC Events", "readOnlyHint": True})
    async def get_events(fabric_name: str = "", limit: int = 100) -> ResourceList:
        """Retrieve recent events from NDFC.

        Args:
            fabric_name: Filter events to a specific fabric (empty = all fabrics).
            limit: Maximum number of events to return (default 100).
        """
        # TODO: implement
        raise NotImplementedError
