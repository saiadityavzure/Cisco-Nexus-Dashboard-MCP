"""Tools: VRF Management.

get_vrfs, get_vrf_attachments, create_vrf, attach_vrf,
deploy_vrfs, detach_vrf, delete_vrf
"""

import logging
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolError

from ..types import ResourceDict, ResourceList
from .dependencies import get_ndfc_client_dep, resolve_vrf

logger = logging.getLogger(__name__)


def register_tools(mcp: FastMCP) -> None:

    @mcp.tool(annotations={"title": "List VRFs", "readOnlyHint": True})
    async def get_vrfs(fabric_name: str) -> ResourceList:
        """List all VRFs in a fabric.

        Args:
            fabric_name: Name of the fabric.
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Get VRF Attachments", "readOnlyHint": True})
    async def get_vrf_attachments(fabric_name: str, vrf_name: str) -> ResourceList:
        """Get the switch attachment state for a VRF.

        Args:
            fabric_name: Name of the fabric.
            vrf_name: Name of the VRF.
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Create VRF"})
    async def create_vrf(fabric_name: str, vrf_name: str, vrf_id: int) -> ResourceDict:
        """Create a new VRF in a fabric.

        Args:
            fabric_name: Name of the fabric.
            vrf_name: Name for the new VRF.
            vrf_id: Unique VRF ID (L3 VNI).
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Attach VRF to Switches"})
    async def attach_vrf(fabric_name: str, vrf_name: str, attach_list: list[dict[str, Any]]) -> ResourceDict:
        """Attach a VRF to one or more switches.

        Args:
            fabric_name: Name of the fabric.
            vrf_name: Name of the VRF.
            attach_list: List of attach entries (serialNumber, vlan, etc.).
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Deploy VRFs"})
    async def deploy_vrfs(fabric_name: str, vrf_names: list[str]) -> ResourceDict:
        """Deploy one or more VRFs to their attached switches.

        Args:
            fabric_name: Name of the fabric.
            vrf_names: List of VRF names to deploy.
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Detach VRF from Switches"})
    async def detach_vrf(fabric_name: str, vrf_name: str, detach_list: list[dict[str, Any]]) -> ResourceDict:
        """Detach a VRF from one or more switches.

        Args:
            fabric_name: Name of the fabric.
            vrf_name: Name of the VRF.
            detach_list: List of detach entries (serialNumber, vlan, etc.).
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "Delete VRF"})
    async def delete_vrf(fabric_name: str, vrf_name: str) -> ResourceDict:
        """Delete a VRF from a fabric. The VRF must be detached from all switches first.

        Args:
            fabric_name: Name of the fabric.
            vrf_name: Name of the VRF to delete.
        """
        # TODO: implement
        raise NotImplementedError
