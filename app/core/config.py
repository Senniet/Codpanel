from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "CodPanel"
    APP_VERSION: str = "0.1.0"

    SERVER_NAME: str = "COD1 Server"

    SERVER_PATH: str = "/data/myserver"
    SERVER_BINARY: str = "/data/myserver/cod_lnxded"
    SERVER_CONFIG: str = "myserver.cfg"

    SERVER_IP: str = "172.16.0.4"
    SERVER_PORT: int = 28960

    SERVER_USER: str = "codserver"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()
