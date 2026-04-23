"""Tools: Switch Management.

get_switches, get_switch_detail, get_switch_policies, apply_freeform,
rediscover_switch, maintenance_mode, get_templates
"""

import logging

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolError

from ..types import ResourceDict, ResourceList
from .dependencies import get_ndfc_client_dep, resolve_switch

logger = logging.getLogger(__name__)


def register_tools(mcp: FastMCP) -> None:

    @mcp.tool(annotations={"title": "List Switches", "readOnlyHint": True})
    async def get_switches(fabric_name: str) -> ResourceList:
        """List all switches in a fabric.

        Args:
            fabric_name: Name of the fabric.
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Get Switch Detail", "readOnlyHint": True})
    async def get_switch_detail(fabric_name: str, switch: str) -> ResourceDict:
        """Get detailed information for a single switch.

        Args:
            fabric_name: Name of the fabric.
            switch: Switch hostname or serial number.
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Get Switch Policies", "readOnlyHint": True})
    async def get_switch_policies(fabric_name: str, switch: str) -> ResourceList:
        """Get the policies applied to a switch.

        Args:
            fabric_name: Name of the fabric.
            switch: Switch hostname or serial number.
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Apply Freeform Config"})
    async def apply_freeform(fabric_name: str, switch: str, config: str) -> ResourceDict:
        """Apply a freeform (raw CLI) configuration snippet to a switch.

        Args:
            fabric_name: Name of the fabric.
            switch: Switch hostname or serial number.
            config: Raw NX-OS CLI configuration block.
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Rediscover Switch"})
    async def rediscover_switch(fabric_name: str, switch: str) -> ResourceDict:
        """Trigger a rediscovery of a switch to sync its state with NDFC.

        Args:
            fabric_name: Name of the fabric.
            switch: Switch hostname or serial number.
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Toggle Maintenance Mode"})
    async def maintenance_mode(fabric_name: str, switch: str, enable: bool) -> ResourceDict:
        """Put a switch into or take it out of maintenance mode.

        Args:
            fabric_name: Name of the fabric.
            switch: Switch hostname or serial number.
            enable: True to enable maintenance mode, False to disable.
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Get Config Templates", "readOnlyHint": True})
    async def get_templates(filter: str = "") -> ResourceList:
        """List available NDFC configuration templates.

        Args:
            filter: Optional substring to filter template names.
        """
        # TODO: implement
        raise NotImplementedError
