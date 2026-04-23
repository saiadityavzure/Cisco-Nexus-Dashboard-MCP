import logging
from typing import Any

import httpx

from .settings import settings

logger = logging.getLogger(__name__)

# API base path — the middleware/proxy layer exposes all routes under /api
_API_BASE = "/api"


class NDFCClient:
    """Thin async HTTP client for the NDFC REST API.

    Auth: API-key via X-Auth-Token header (no login call needed).
    All methods raise httpx.HTTPStatusError on non-2xx responses.
    Tools never import httpx directly.
    """

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "NDFCClient":
        self._client = httpx.AsyncClient(
            base_url=settings.ndfc_host,
            verify=settings.ndfc_verify_ssl,
            timeout=60.0,
        )
        return self

    async def __aexit__(self, *_: Any) -> None:
        if self._client:
            await self._client.aclose()

    def _headers(self) -> dict[str, str]:
        return {"X-Auth-Token": settings.ndfc_api_key, "Content-Type": "application/json"}

    def _url(self, endpoint: str) -> str:
        """Prepend the API base if the caller passed a short path."""
        if endpoint.startswith("/api"):
            return endpoint
        return f"{_API_BASE}{endpoint}"

    async def get(self, endpoint: str, params: dict | None = None) -> Any:
        resp = await self._client.get(self._url(endpoint), headers=self._headers(), params=params)
        resp.raise_for_status()
        return resp.json() if resp.content else None

    async def post(self, endpoint: str, data: Any = None) -> Any:
        resp = await self._client.post(self._url(endpoint), headers=self._headers(), json=data)
        resp.raise_for_status()
        return resp.json() if resp.content else None

    async def put(self, endpoint: str, data: Any = None) -> Any:
        resp = await self._client.put(self._url(endpoint), headers=self._headers(), json=data)
        resp.raise_for_status()
        return resp.json() if resp.content else None

    async def patch(self, endpoint: str, data: Any = None) -> Any:
        resp = await self._client.patch(self._url(endpoint), headers=self._headers(), json=data)
        resp.raise_for_status()
        return resp.json() if resp.content else None

    async def delete(self, endpoint: str) -> Any:
        resp = await self._client.delete(self._url(endpoint), headers=self._headers())
        resp.raise_for_status()
        return resp.json() if resp.content else None


# Singleton used in stdio mode; overridden per-request in SSE/HTTP mode
_client: NDFCClient | None = None


def get_ndfc_client() -> NDFCClient:
    global _client
    if _client is None:
        _client = NDFCClient()
    return _client
