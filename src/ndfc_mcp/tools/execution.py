"""Tools: NX-API / SSH Execution.

nxapi_exec, nxapi_bulk, ssh_exec, ssh_bulk
"""

import logging

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolError

from ..types import ResourceDict, ResourceList
from .dependencies import get_ndfc_client_dep

logger = logging.getLogger(__name__)


def register_tools(mcp: FastMCP) -> None:

    @mcp.tool(annotations={"title": "NX-API Execute (Single)"})
    async def nxapi_exec(host: str, command: str, command_type: str = "cli") -> ResourceDict:
        """Execute a single NX-API command on a switch.

        Args:
            host: Switch IP address or hostname.
            command: NX-OS CLI or bash command to run.
            command_type: Command type — "cli" (default) or "bash".
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "NX-API Execute (Bulk)"})
    async def nxapi_bulk(hosts: list[str], command: str, command_type: str = "cli") -> ResourceList:
        """Execute a NX-API command on multiple switches in parallel.

        Args:
            hosts: List of switch IP addresses or hostnames.
            command: NX-OS CLI or bash command to run.
            command_type: Command type — "cli" (default) or "bash".
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "SSH Execute (Single)"})
    async def ssh_exec(host: str, command: str, username: str = "", password: str = "") -> ResourceDict:
        """Run a command on a single host over SSH.

        Args:
            host: Target hostname or IP address.
            command: Shell command to execute.
            username: SSH username (falls back to settings.ssh_username).
            password: SSH password (falls back to settings.ssh_password).
        """
        # TODO: implement
        raise NotImplementedError

    @mcp.tool(annotations={"title": "SSH Execute (Bulk)"})
    async def ssh_bulk(
        hosts: list[str], command: str, username: str = "", password: str = ""
    ) -> ResourceList:
        """Run a command on multiple hosts over SSH in parallel.

        Args:
            hosts: List of target hostnames or IP addresses.
            command: Shell command to execute.
            username: SSH username (falls back to settings.ssh_username).
            password: SSH password (falls back to settings.ssh_password).
        """
        # TODO: implement
        raise NotImplementedError
