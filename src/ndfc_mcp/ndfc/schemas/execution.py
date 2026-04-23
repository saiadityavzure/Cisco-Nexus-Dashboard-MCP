"""Pydantic models for NX-API and SSH execution request/response bodies."""

from pydantic import BaseModel


class NxapiRequest(BaseModel, extra="forbid"):
    host: str
    command: str
    command_type: str = "cli"  # "cli" | "bash"


class NxapiBulkRequest(BaseModel, extra="forbid"):
    hosts: list[str]
    command: str
    command_type: str = "cli"


class NxapiResult(BaseModel, extra="ignore"):
    host: str | None = None
    output: str | None = None
    error: str | None = None
    success: bool = False


class SshRequest(BaseModel, extra="forbid"):
    host: str
    command: str
    username: str = ""
    password: str = ""
    timeout: int = 30


class SshBulkRequest(BaseModel, extra="forbid"):
    hosts: list[str]
    command: str
    username: str = ""
    password: str = ""
    timeout: int = 30


class SshResult(BaseModel, extra="ignore"):
    host: str | None = None
    stdout: str | None = None
    stderr: str | None = None
    returncode: int | None = None
    success: bool = False
