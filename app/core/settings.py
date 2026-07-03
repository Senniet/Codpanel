from pathlib import Path
import tomllib


BASE_DIR = Path(__file__).resolve().parents[2]

CONFIG_FILE = BASE_DIR / "config.toml"


class Settings:

    def __init__(self):

        with open(CONFIG_FILE, "rb") as f:
            self.config = tomllib.load(f)

    @property
    def app(self):
        return self.config["application"]

    @property
    def server(self):
        return self.config["server"]


settings = Settings()
