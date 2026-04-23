"""Tools: Network Management.

get_networks, get_network_attachments, create_network, attach_network,
detach_network, deploy_networks, delete_network
"""

import logging
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from ..types import ResourceDict, ResourceList
from .dependencies import get_ndfc_client_dep, resolve_network

logger = logging.getLogger(__name__)


def register_tools(mcp: FastMCP) -> None:

    @mcp.tool(annotations={"title": "List Networks", "readOnlyHint": True})
    async def get_networks(fabric_name: str) -> ResourceList:
        """List all networks in a fabric.

        Args:
            fabric_name: Name of the fabric.
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Get Network Attachments", "readOnlyHint": True})
    async def get_network_attachments(fabric_name: str, network_name: str) -> ResourceList:
        """Get the switch attachment state for a network.

        Args:
            fabric_name: Name of the fabric.
            network_name: Name of the network.
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Create Network"})
    async def create_network(
        fabric_name: str, network_name: str, network_id: int, vrf_name: str = ""
    ) -> ResourceDict:
        """Create a new L2/L3 network in a fabric.

        Args:
            fabric_name: Name of the fabric.
            network_name: Name for the new network.
            network_id: Unique network ID (L2 VNI).
            vrf_name: VRF to associate the network with (empty for L2-only).
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Attach Network to Switches"})
    async def attach_network(
        fabric_name: str, network_name: str, attach_list: list[dict[str, Any]]
    ) -> ResourceDict:
        """Attach a network to one or more switches.

        Args:
            fabric_name: Name of the fabric.
            network_name: Name of the network.
            attach_list: List of attach entries (serialNumber, vlan, portNames, etc.).
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Detach Network from Switches"})
    async def detach_network(
        fabric_name: str, network_name: str, detach_list: list[dict[str, Any]]
    ) -> ResourceDict:
        """Detach a network from one or more switches.

        Args:
            fabric_name: Name of the fabric.
            network_name: Name of the network.
            detach_list: List of detach entries (serialNumber, vlan, etc.).
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Deploy Networks"})
    async def deploy_networks(fabric_name: str, network_names: list[str]) -> ResourceDict:
        """Deploy one or more networks to their attached switches.

        Args:
            fabric_name: Name of the fabric.
            network_names: List of network names to deploy.
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Delete Network"})
    async def delete_network(fabric_name: str, network_name: str) -> ResourceDict:
        """Delete a network from a fabric. The network must be detached from all switches first.

        Args:
            fabric_name: Name of the fabric.
            network_name: Name of the network to delete.
        """
        # TODO: implement
        raise NotImplementedError
