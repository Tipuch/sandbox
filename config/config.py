from typing import Literal
from fastapi.templating import Jinja2Templates
from inertia import InertiaConfig
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine


class Config(BaseSettings):
    ENVIRONMENT: Literal["development", "production"] = "development"
    TEMPLATES_DIR: Path = Path("./templates").resolve()

    MANIFEST_JSON: Path = Path("./static/dist/manifest.json").resolve()
    SVELTE_DIR: Path = Path("./static/src").resolve()

    sqlite_file_name: str = "database.db"
    DB_URL: str = f"sqlite:///{sqlite_file_name}"
    SECRET_KEY: str = "very_secret_key_make_sure_to_change_it_in_prod"
    ACTIVATION_MAX_AGE: int = 3600 * 24  # 24 hours for the activation link
    PYOTP_INTERVAL: int = 30
    JWT_ALGORITHM: str = "HS512"
    JWT_EXPIRATION_MINUTES: int = 1440

    model_config = SettingsConfigDict(env_file=".env")

    def get_templates(self):
        return Jinja2Templates(directory=self.TEMPLATES_DIR)

    def init_db(self):
        connect_args = {"check_same_thread": False}
        return create_engine(self.DB_URL, echo=True, connect_args=connect_args)

    def get_inertia_config(self) -> InertiaConfig:
        return InertiaConfig(
            templates=self.get_templates(),
            manifest_json_path=str(self.MANIFEST_JSON),
            environment=self.ENVIRONMENT,
            use_flash_messages=True,
            use_flash_errors=True,
            entrypoint_filename="main.js",
            assets_prefix="/src",
        )


settings = Config()
