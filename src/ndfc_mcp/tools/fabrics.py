"""Tools: Fabric Management.

get_fabrics, get_fabric_summary, get_fabric_detail, create_fabric,
delete_fabric, get_topology, get_full_topology, get_fabric_inventory,
get_compliance, config_save, config_deploy, recalculate_and_deploy, config_preview
"""

import logging
from urllib.parse import quote

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolError

from ..types import ResourceDict, ResourceList
from .dependencies import get_ndfc_client_dep, resolve_fabric, run_with_heartbeat

logger = logging.getLogger(__name__)

_VALID_FABRIC_TYPES = {
    "switch_fabric": "Switch_Fabric",
    "external_fabric": "External_Fabric",
    "lan_classic": "LAN_Classic",
    "msd_fabric": "MSD_Fabric",
}


def _required_arg(value: str, name: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ToolError(f"'{name}' is required.")
    return cleaned


def _normalize_fabric_type(fabric_type: str) -> str:
    key = _required_arg(fabric_type, "fabric_type").replace("-", "_").lower()
    canonical = _VALID_FABRIC_TYPES.get(key)
    if canonical:
        return canonical

    allowed = ", ".join(_VALID_FABRIC_TYPES.values())
    raise ToolError(f"Invalid fabric_type '{fabric_type}'. Allowed values: {allowed}")


def _path(value: str) -> str:
    return quote(value, safe="")


def register_tools(mcp: FastMCP) -> None:

    @mcp.tool(annotations={"title": "List Fabrics", "readOnlyHint": True})
    async def get_fabrics() -> ResourceList:
        """List all fabrics managed by NDFC."""
        client = get_ndfc_client_dep()
        try:
            resp = await client.get("/api/fabrics")
            return resp if isinstance(resp, list) else []
        except ToolError:
            raise
        except httpx.HTTPStatusError as e:
            raise ToolError(f"HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            logger.error("get_fabrics failed", exc_info=True)
            raise ToolError(str(e))

    @mcp.tool(annotations={"title": "Create Fabric"})
    async def create_fabric(fabric_name: str, fabric_type: str, nv_pairs: dict | None = None) -> ResourceDict:
        """Create a new fabric in NDFC.

        Args:
            fabric_name: Unique name for the new fabric (no spaces).
            fabric_type: Fabric type — Switch_Fabric, External_Fabric, LAN_Classic, MSD_Fabric.
            nv_pairs: Optional fabric template parameter overrides as key-value pairs.
        """
        client = get_ndfc_client_dep()
        try:
            name = _required_arg(fabric_name, "fabric_name")
            if any(ch.isspace() for ch in name):
                raise ToolError("'fabric_name' cannot contain spaces.")

            if nv_pairs is not None and not isinstance(nv_pairs, dict):
                raise ToolError("'nv_pairs' must be a dictionary when provided.")

            payload: dict = {
                "fabricName": name,
                "fabricType": _normalize_fabric_type(fabric_type),
            }
            if nv_pairs:
                payload["nvPairs"] = nv_pairs
            resp = await client.post("/api/fabrics", data=payload)
            return resp if isinstance(resp, dict) else {"fabricName": name, "status": "created"}
        except ToolError:
            raise
        except httpx.HTTPStatusError as e:
            raise ToolError(f"HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            logger.error("create_fabric failed", exc_info=True)
            raise ToolError(str(e))

    @mcp.tool(annotations={"title": "Delete Fabric"})
    async def delete_fabric(fabric_name: str) -> ResourceDict:
        """Delete a fabric from NDFC. All switches must be removed from the fabric first.

        Args:
            fabric_name: Name of the fabric to delete.
        """
        client = get_ndfc_client_dep()
        try:
            name = _required_arg(fabric_name, "fabric_name")
            fname = await resolve_fabric(name, client)
            await client.delete(f"/api/fabrics/{_path(fname)}")
            return {"fabricName": fname, "status": "deleted"}
        except ToolError:
            raise
        except httpx.HTTPStatusError as e:
            raise ToolError(f"HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            logger.error("delete_fabric failed", exc_info=True)
            raise ToolError(str(e))

    @mcp.tool(annotations={"title": "Get Fabric Summary", "readOnlyHint": True})
    async def get_fabric_summary(fabric_name: str) -> ResourceDict:
        """Get a high-level summary of a fabric (switch count, VRF/network counts, health).

        Args:
            fabric_name: Name of the fabric.
        """
        client = get_ndfc_client_dep()
        try:
            name = _required_arg(fabric_name, "fabric_name")
            fname = await resolve_fabric(name, client)
            resp = await client.get(f"/api/fabrics/{_path(fname)}/summary")
            return resp if isinstance(resp, dict) else {"raw": resp}
        except ToolError:
            raise
        except httpx.HTTPStatusError as e:
            raise ToolError(f"HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            logger.error("get_fabric_summary failed", exc_info=True)
            raise ToolError(str(e))

    @mcp.tool(annotations={"title": "Get Fabric Detail", "readOnlyHint": True})
    async def get_fabric_detail(fabric_name: str) -> ResourceDict:
        """Get full fabric detail including all nvPairs configuration.

        Args:
            fabric_name: Name of the fabric.
        """
        client = get_ndfc_client_dep()
        try:
            name = _required_arg(fabric_name, "fabric_name")
            fname = await resolve_fabric(name, client)
            resp = await client.get(f"/api/fabrics/{_path(fname)}/detail")
            return resp if isinstance(resp, dict) else {"raw": resp}
        except ToolError:
            raise
        except httpx.HTTPStatusError as e:
            raise ToolError(f"HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            logger.error("get_fabric_detail failed", exc_info=True)
            raise ToolError(str(e))

    @mcp.tool(annotations={"title": "Get Fabric Topology", "readOnlyHint": True})
    async def get_topology(fabric_name: str) -> ResourceDict:
        """Get the topology (nodes and links) for a specific fabric.

        Args:
            fabric_name: Name of the fabric.
        """
        client = get_ndfc_client_dep()
        try:
            name = _required_arg(fabric_name, "fabric_name")
            fname = await resolve_fabric(name, client)
            resp = await client.get(f"/api/fabrics/{_path(fname)}/topology")
            return resp if isinstance(resp, dict) else {"raw": resp}
        except ToolError:
            raise
        except httpx.HTTPStatusError as e:
            raise ToolError(f"HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            logger.error("get_topology failed", exc_info=True)
            raise ToolError(str(e))

    @mcp.tool(annotations={"title": "Get Full Topology", "readOnlyHint": True})
    async def get_full_topology() -> ResourceDict:
        """Get the complete multi-fabric topology across all fabrics."""
        client = get_ndfc_client_dep()
        try:
            resp = await client.get("/api/topology/full")
            return resp if isinstance(resp, dict) else {"raw": resp}
        except ToolError:
            raise
        except httpx.HTTPStatusError as e:
            raise ToolError(f"HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            logger.error("get_full_topology failed", exc_info=True)
            raise ToolError(str(e))

    @mcp.tool(annotations={"title": "Get Fabric Inventory", "readOnlyHint": True})
    async def get_fabric_inventory(fabric_name: str) -> ResourceList:
        """Get the switch inventory for a fabric.

        Args:
            fabric_name: Name of the fabric.
        """
        client = get_ndfc_client_dep()
        try:
            name = _required_arg(fabric_name, "fabric_name")
            fname = await resolve_fabric(name, client)
            resp = await client.get(f"/api/fabrics/{_path(fname)}/inventory")
            return resp if isinstance(resp, list) else []
        except ToolError:
            raise
        except httpx.HTTPStatusError as e:
            raise ToolError(f"HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            logger.error("get_fabric_inventory failed", exc_info=True)
            raise ToolError(str(e))

    @mcp.tool(annotations={"title": "Get Config Compliance", "readOnlyHint": True})
    async def get_compliance(fabric_name: str) -> ResourceList:
        """Get the configuration compliance status for all switches in a fabric.

        Args:
            fabric_name: Name of the fabric.
        """
        client = get_ndfc_client_dep()
        try:
            name = _required_arg(fabric_name, "fabric_name")
            fname = await resolve_fabric(name, client)
            resp = await client.get(f"/api/fabrics/{_path(fname)}/compliance")
            return resp if isinstance(resp, list) else []
        except ToolError:
            raise
        except httpx.HTTPStatusError as e:
            raise ToolError(f"HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            logger.error("get_compliance failed", exc_info=True)
            raise ToolError(str(e))

    @mcp.tool(annotations={"title": "Save Fabric Config"})
    async def config_save(fabric_name: str) -> ResourceDict:
        """Save (stage) the current intended configuration for a fabric.

        Args:
            fabric_name: Name of the fabric.
        """
        client = get_ndfc_client_dep()
        try:
            name = _required_arg(fabric_name, "fabric_name")
            fname = await resolve_fabric(name, client)
            resp = await client.post(f"/api/fabrics/{_path(fname)}/config-save")
            return resp if isinstance(resp, dict) else {"fabricName": fname, "status": "saved"}
        except ToolError:
            raise
        except httpx.HTTPStatusError as e:
            raise ToolError(f"HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            logger.error("config_save failed", exc_info=True)
            raise ToolError(str(e))

    @mcp.tool(annotations={"title": "Deploy Fabric Config"})
    async def config_deploy(fabric_name: str, ctx=None) -> ResourceDict:
        """Deploy the staged configuration to all switches in a fabric.

        Args:
            fabric_name: Name of the fabric.
        """
        client = get_ndfc_client_dep()
        try:
            name = _required_arg(fabric_name, "fabric_name")
            fname = await resolve_fabric(name, client)
            coro = client.post(f"/api/fabrics/{_path(fname)}/config-deploy")
            resp = await run_with_heartbeat(coro, ctx) if ctx else await coro
            return resp if isinstance(resp, dict) else {"fabricName": fname, "status": "deployed"}
        except ToolError:
            raise
        except httpx.HTTPStatusError as e:
            raise ToolError(f"HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            logger.error("config_deploy failed", exc_info=True)
            raise ToolError(str(e))

    @mcp.tool(annotations={"title": "Recalculate & Deploy"})
    async def recalculate_and_deploy(fabric_name: str, ctx=None) -> ResourceDict:
        """Recalculate the intended config and deploy it to all switches in a fabric.

        Equivalent to clicking 'Recalculate & Deploy' in the NDFC UI.

        Args:
            fabric_name: Name of the fabric.
        """
        client = get_ndfc_client_dep()
        try:
            name = _required_arg(fabric_name, "fabric_name")
            fname = await resolve_fabric(name, client)
            coro = client.post(f"/api/fabrics/{_path(fname)}/recalculate-deploy")
            resp = await run_with_heartbeat(coro, ctx) if ctx else await coro
            return resp if isinstance(resp, dict) else {"fabricName": fname, "status": "recalculated_and_deployed"}
        except ToolError:
            raise
        except httpx.HTTPStatusError as e:
            raise ToolError(f"HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            logger.error("recalculate_and_deploy failed", exc_info=True)
            raise ToolError(str(e))

    @mcp.tool(annotations={"title": "Preview Pending Config", "readOnlyHint": True})
    async def config_preview(fabric_name: str, serial_number: str) -> ResourceDict:
        """Preview the pending configuration diff for a specific switch in a fabric.

        Args:
            fabric_name: Name of the fabric.
            serial_number: Switch serial number to preview config for.
        """
        client = get_ndfc_client_dep()
        try:
            name = _required_arg(fabric_name, "fabric_name")
            serial = _required_arg(serial_number, "serial_number")
            fname = await resolve_fabric(name, client)
            resp = await client.get(
                f"/api/fabrics/{_path(fname)}/config-preview/{_path(serial)}"
            )
            return resp if isinstance(resp, dict) else {"raw": resp}
        except ToolError:
            raise
        except httpx.HTTPStatusError as e:
            raise ToolError(f"HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            logger.error("config_preview failed", exc_info=True)
            raise ToolError(str(e))
