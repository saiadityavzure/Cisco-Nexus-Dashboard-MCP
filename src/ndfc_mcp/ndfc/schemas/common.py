"""Shared types, enums, and annotated aliases used across all schema modules."""

from enum import StrEnum
from typing import Annotated

from pydantic import BeforeValidator, Field


def _strip(v: str) -> str:
    return v.strip() if isinstance(v, str) else v


FabricName = Annotated[str, BeforeValidator(_strip), Field(min_length=1, max_length=64)]
SwitchSerial = Annotated[str, BeforeValidator(_strip), Field(min_length=1)]
VrfName = Annotated[str, BeforeValidator(_strip), Field(min_length=1, max_length=32)]
NetworkName = Annotated[str, BeforeValidator(_strip), Field(min_length=1, max_length=32)]


class FabricType(StrEnum):
    VXLAN_EVPN = "Switch_Fabric"
    EXTERNAL = "External_Fabric"
    LAN_CLASSIC = "LAN_Classic"
    MSD = "MSD_Fabric"


class DeploymentStatus(StrEnum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    OUT_OF_SYNC = "Out-of-Sync"


class SwitchRole(StrEnum):
    SPINE = "spine"
    LEAF = "leaf"
    BORDER = "border"
    BORDER_SPINE = "border spine"
    BORDER_LEAF = "border leaf"
    ACCESS = "access"


class VrfState(StrEnum):
    DEPLOYED = "DEPLOYED"
    PENDING = "PENDING"
    OUT_OF_SYNC = "OUT-OF-SYNC"
    NA = "NA"


class NetworkState(StrEnum):
    DEPLOYED = "DEPLOYED"
    PENDING = "PENDING"
    OUT_OF_SYNC = "OUT-OF-SYNC"
    NA = "NA"
