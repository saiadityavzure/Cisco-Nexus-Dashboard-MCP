"""Pydantic models for Troubleshooting, Alarms, and Events API bodies."""

from pydantic import BaseModel


class Alarm(BaseModel, extra="ignore"):
    alarmId: str | None = None
    severity: str | None = None
    source: str | None = None
    description: str | None = None
    createdAt: str | None = None
    acknowledgedAt: str | None = None
    state: str | None = None


class Event(BaseModel, extra="ignore"):
    eventId: str | None = None
    severity: str | None = None
    source: str | None = None
    description: str | None = None
    createdAt: str | None = None
    category: str | None = None


class TroubleshootSummary(BaseModel, extra="ignore"):
    fabricName: str | None = None
    switchCount: int | None = None
    activeAlarms: int | None = None
    complianceErrors: int | None = None
    unreachableSwitches: int | None = None
