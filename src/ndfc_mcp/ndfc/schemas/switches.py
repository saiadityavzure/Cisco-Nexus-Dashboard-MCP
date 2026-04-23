"""Pydantic models for Switch REST API request/response bodies."""

from pydantic import BaseModel

from .common import SwitchRole, SwitchSerial


class Switch(BaseModel, extra="ignore"):
    serialNumber: str | None = None
    logicalName: str | None = None
    ipAddress: str | None = None
    model: str | None = None
    release: str | None = None
    role: SwitchRole | None = None
    fabricName: str | None = None
    operStatus: str | None = None
    mode: str | None = None


class SwitchDetail(Switch, extra="ignore"):
    systemUpTime: str | None = None
    lastUpdated: str | None = None
    interfaces: list[str] = []


class SwitchPolicy(BaseModel, extra="ignore"):
    policyId: str | None = None
    serialNumber: str | None = None
    templateName: str | None = None
    description: str | None = None
    generatedConfig: str | None = None


class FreeformConfigApply(BaseModel, extra="forbid"):
    serialNumber: SwitchSerial
    freeformConfig: str


class MaintenanceModeRequest(BaseModel, extra="forbid"):
    serialNumber: SwitchSerial
    mode: str  # "maintenance" | "normal"


class Template(BaseModel, extra="ignore"):
    name: str | None = None
    description: str | None = None
    templateType: str | None = None
    parameters: list[dict] = []
