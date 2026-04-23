from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # NDFC connection — API-key auth (no password needed)
    ndfc_host: str
    ndfc_username: str = "admin"
    ndfc_api_key: str = ""
    ndfc_password: str = ""          # kept as fallback if API key absent
    ndfc_verify_ssl: bool = False

    # ND compatibility aliases
    nd_url: str = ""
    nd_username: str = ""
    nd_verify_ssl: bool = False

    # Transport mode: "stdio" or "http"
    transport: str = "stdio"

    # HTTP server (only used when transport="http")
    host: str = "0.0.0.0"
    port: int = 9007

    # MCP transport security (Host/Origin validation for HTTP/SSE transport)
    enable_dns_rebinding_protection: bool = True
    allowed_hosts: str = ""
    allowed_origins: str = ""

    # SSH defaults (for ssh_exec / ssh_bulk tools)
    ssh_username: str = ""
    ssh_password: str = ""
    ssh_timeout: int = 30

    # NX-API defaults
    nxapi_port: int = 443
    nxapi_verify_ssl: bool = False

    # Tool group toggles
    enable_execution_tools: bool = True
    enable_troubleshooting_tools: bool = True
    enable_write_tools: bool = True

    @staticmethod
    def _csv_to_list(value: str) -> list[str]:
        return [item.strip() for item in value.split(",") if item.strip()]

    @property
    def allowed_hosts_list(self) -> list[str]:
        return self._csv_to_list(self.allowed_hosts)

    @property
    def allowed_origins_list(self) -> list[str]:
        explicit = self._csv_to_list(self.allowed_origins)
        if explicit:
            return explicit

        # If origins are not explicitly provided, derive them from allowed hosts.
        # This keeps config simple while preserving Host/Origin validation.
        derived: list[str] = []
        for host in self.allowed_hosts_list:
            # If the value already looks like a URL, keep it.
            if host.startswith("http://") or host.startswith("https://"):
                if host not in derived:
                    derived.append(host)
                continue

            http_origin = f"http://{host}"
            https_origin = f"https://{host}"
            if http_origin not in derived:
                derived.append(http_origin)
            if https_origin not in derived:
                derived.append(https_origin)

        return derived


settings = Settings()
