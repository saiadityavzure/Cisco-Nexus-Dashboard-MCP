"""Shared helpers injected into every tool function.

- Client dependency injection
- Name resolution helpers
- Heartbeat wrapper for long-running ops
"""

import asyncio
import logging
import unicodedata

from mcp.types import ToolError

from ..ndfc_client import NDFCClient, get_ndfc_client

logger = logging.getLogger(__name__)

# API base paths
_FABRIC_BASE = "/api/fabrics"


def get_ndfc_client_dep() -> NDFCClient:
    return get_ndfc_client()


def _normalize(name: str) -> str:
    return unicodedata.normalize("NFKC", name).strip().lower()


async def resolve_fabric(fabric_name: str, client: NDFCClient) -> str:
    """Validate that the fabric exists and return its canonical name.

    NDFC uses fabric names (not UUIDs) as identifiers, so this is a
    presence check + canonical-name lookup to handle case/whitespace mismatches.
    """
    try:
        fabrics = await client.get("/api/fabrics")
    except Exception as e:
        raise ToolError(f"Failed to list fabrics while resolving '{fabric_name}': {e}")

    if not isinstance(fabrics, list):
        raise ToolError("Unexpected response format from NDFC fabric list.")

    target = _normalize(fabric_name)
    for f in fabrics:
        name = f.get("fabricName", "")
        if _normalize(name) == target:
            return name

    known = [f.get("fabricName", "") for f in fabrics]
    raise ToolError(f"Fabric '{fabric_name}' not found. Known fabrics: {known}")


async def resolve_switch(serial_or_name: str, fabric_name: str, client: NDFCClient) -> str:
    """Resolve a switch hostname or serial number to its serialNumber within a fabric."""
    try:
        switches = await client.get(f"/api/fabrics/{fabric_name}/inventory")
    except Exception as e:
        raise ToolError(f"Failed to list switches for fabric '{fabric_name}': {e}")

    if not isinstance(switches, list):
        raise ToolError("Unexpected response format from NDFC inventory.")

    target = _normalize(serial_or_name)
    for sw in switches:
        if _normalize(sw.get("serialNumber", "")) == target:
            return sw["serialNumber"]
        if _normalize(sw.get("logicalName", "")) == target:
            return sw["serialNumber"]
        if _normalize(sw.get("ipAddress", "")) == target:
            return sw["serialNumber"]

    raise ToolError(
        f"Switch '{serial_or_name}' not found in fabric '{fabric_name}'. "
        f"Provide a serial number, hostname, or IP address."
    )


async def resolve_vrf(vrf_name: str, fabric_name: str, client: NDFCClient) -> str:
    """Validate VRF exists in the fabric and return its canonical name."""
    try:
        vrfs = await client.get(f"/api/vrfs?fabric={fabric_name}")
    except Exception as e:
        raise ToolError(f"Failed to list VRFs for fabric '{fabric_name}': {e}")

    if not isinstance(vrfs, list):
        raise ToolError("Unexpected response format from NDFC VRF list.")

    target = _normalize(vrf_name)
    for v in vrfs:
        name = v.get("vrfName", "")
        if _normalize(name) == target:
            return name

    raise ToolError(f"VRF '{vrf_name}' not found in fabric '{fabric_name}'.")


async def resolve_network(network_name: str, fabric_name: str, client: NDFCClient) -> str:
    """Validate network exists in the fabric and return its canonical name."""
    try:
        networks = await client.get(f"/api/networks?fabric={fabric_name}")
    except Exception as e:
        raise ToolError(f"Failed to list networks for fabric '{fabric_name}': {e}")

    if not isinstance(networks, list):
        raise ToolError("Unexpected response format from NDFC network list.")

    target = _normalize(network_name)
    for n in networks:
        name = n.get("networkName", "")
        if _normalize(name) == target:
            return name

    raise ToolError(f"Network '{network_name}' not found in fabric '{fabric_name}'.")


async def run_with_heartbeat(coro, ctx):
    """Wrap a slow awaitable with periodic SSE keepalive pings.

    Prevents the MCP client from timing out on long-running NDFC operations
    such as config deploy or recalculate & deploy.
    """
    async def _heartbeat():
        while True:
            await asyncio.sleep(5)
            try:
                await ctx.report_progress(0, 0)
            except Exception:
                pass

    task = asyncio.create_task(_heartbeat())
    try:
        return await coro
    finally:
        task.cancel()
