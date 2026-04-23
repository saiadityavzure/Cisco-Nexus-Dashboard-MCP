"""Tools: Interface Management.

get_interfaces, provision_interface, deploy_interfaces
"""

import logging
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolError

from ..types import ResourceDict, ResourceList
from .dependencies import get_ndfc_client_dep

logger = logging.getLogger(__name__)


def register_tools(mcp: FastMCP) -> None:

    @mcp.tool(annotations={"title": "List Interfaces", "readOnlyHint": True})
    async def get_interfaces(fabric_name: str, switch: str) -> ResourceList:
        """List all interfaces on a switch.

        Args:
            fabric_name: Name of the fabric.
            switch: Switch hostname or serial number.
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Provision Interface"})
    async def provision_interface(
        fabric_name: str,
        switch: str,
        if_name: str,
        policy: str,
        nv_pairs: dict[str, Any] | None = None,
    ) -> ResourceDict:
        """Provision an interface on a switch using an NDFC policy template.

        Args:
            fabric_name: Name of the fabric.
            switch: Switch hostname or serial number.
            if_name: Interface name (e.g. Ethernet1/1).
            policy: NDFC interface policy template name.
            nv_pairs: Policy parameter overrides as key-value pairs.
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Deploy Interface Configs"})
    async def deploy_interfaces(fabric_name: str, switch: str, if_names: list[str]) -> ResourceDict:
        """Deploy pending interface configurations to a switch.

        Args:
            fabric_name: Name of the fabric.
            switch: Switch hostname or serial number.
            if_names: List of interface names to deploy.
        """
        # TODO: implement
        raise NotImplementedError
