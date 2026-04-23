"""Pydantic models for Fabric REST API request/response bodies."""

from typing import Any

from pydantic import BaseModel

from .common import DeploymentStatus, FabricName, FabricType


class FabricCreate(BaseModel, extra="forbid"):
    fabricName: FabricName
    fabricType: FabricType
    # TODO: add remaining required/optional fields per NDFC API spec


class Fabric(BaseModel, extra="ignore"):
    fabricName: str
    fabricType: str | None = None
    fabricTechnology: str | None = None
    deploymentStatus: DeploymentStatus | None = None
    nvPairs: dict[str, Any] | None = None


class FabricSummary(BaseModel, extra="ignore"):
    fabricName: str
    switchCount: int | None = None
    deployedNetworkCount: int | None = None
    deployedVrfCount: int | None = None


class FabricTopologyNode(BaseModel, extra="ignore"):
    serialNumber: str | None = None
    logicalName: str | None = None
    role: str | None = None
    ipAddress: str | None = None


class FabricTopologyLink(BaseModel, extra="ignore"):
    srcNode: str | None = None
    dstNode: str | None = None
    srcInterface: str | None = None
    dstInterface: str | None = None


class FabricTopology(BaseModel, extra="ignore"):
    nodes: list[FabricTopologyNode] = []
    links: list[FabricTopologyLink] = []


class ComplianceStatus(BaseModel, extra="ignore"):
    switchName: str | None = None
    serialNumber: str | None = None
    complianceState: str | None = None
    lastSyncTime: str | None = None
