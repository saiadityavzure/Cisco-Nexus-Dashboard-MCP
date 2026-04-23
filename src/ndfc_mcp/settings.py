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


settings = Settings()
