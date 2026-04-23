"""Pydantic models for VRF REST API request/response bodies."""

from typing import Any

from pydantic import BaseModel

from .common import VrfName, VrfState


class VrfCreate(BaseModel, extra="forbid"):
    fabric: str
    vrfName: VrfName
    vrfId: int
    vrfTemplate: str = "Default_VRF_Universal"
    vrfExtensionTemplate: str = "Default_VRF_Extension_Universal"
    vrfTemplateConfig: dict[str, Any] = {}
    # TODO: add remaining optional fields per NDFC API spec


class Vrf(BaseModel, extra="ignore"):
    fabric: str | None = None
    vrfName: str | None = None
    vrfId: int | None = None
    vrfStatus: VrfState | None = None
    vrfTemplate: str | None = None


class VrfAttachment(BaseModel, extra="ignore"):
    vrfName: str | None = None
    serialNumber: str | None = None
    vlan: int | None = None
    attachState: str | None = None
    isAttached: bool | None = None


class VrfAttachRequest(BaseModel, extra="forbid"):
    vrfName: VrfName
    lanAttachList: list[dict[str, Any]]


class VrfDetachRequest(BaseModel, extra="forbid"):
    vrfName: VrfName
    lanAttachList: list[dict[str, Any]]
