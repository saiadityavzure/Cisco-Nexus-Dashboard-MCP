"""Pydantic models for Network REST API request/response bodies."""

from typing import Any

from pydantic import BaseModel

from .common import NetworkName, NetworkState


class NetworkCreate(BaseModel, extra="forbid"):
    fabric: str
    networkName: NetworkName
    networkId: int
    networkTemplate: str = "Default_Network_Universal"
    networkExtensionTemplate: str = "Default_Network_Extension_Universal"
    networkTemplateConfig: dict[str, Any] = {}
    vrf: str = ""
    # TODO: add remaining optional fields per NDFC API spec


class Network(BaseModel, extra="ignore"):
    fabric: str | None = None
    networkName: str | None = None
    networkId: int | None = None
    networkStatus: NetworkState | None = None
    vrf: str | None = None
    networkTemplate: str | None = None


class NetworkAttachment(BaseModel, extra="ignore"):
    networkName: str | None = None
    serialNumber: str | None = None
    vlan: int | None = None
    portNames: str | None = None
    attachState: str | None = None
    isAttached: bool | None = None


class NetworkAttachRequest(BaseModel, extra="forbid"):
    networkName: NetworkName
    lanAttachList: list[dict[str, Any]]


class NetworkDetachRequest(BaseModel, extra="forbid"):
    networkName: NetworkName
    lanAttachList: list[dict[str, Any]]
