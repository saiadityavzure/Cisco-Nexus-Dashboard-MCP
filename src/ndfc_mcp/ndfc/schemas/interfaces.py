"""Pydantic models for Interface REST API request/response bodies."""

from typing import Any

from pydantic import BaseModel


class Interface(BaseModel, extra="ignore"):
    serialNumber: str | None = None
    ifName: str | None = None
    ifType: str | None = None
    adminState: str | None = None
    operState: str | None = None
    description: str | None = None
    mtu: int | None = None
    speed: str | None = None


class InterfaceProvisionRequest(BaseModel, extra="forbid"):
    serialNumber: str
    ifName: str
    policy: str
    nvPairs: dict[str, Any] = {}


class InterfaceDeployRequest(BaseModel, extra="forbid"):
    serialNumber: str
    ifName: str
