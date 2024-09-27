from inertia import InertiaConfig
from sqlalchemy import create_engine

from .config import Config


class DevConfig(Config):
    sqlite_file_name = "database.db"
    DB_URL = f"sqlite:///{sqlite_file_name}"
    SECRET_KEY = "very_secret_key_make_sure_to_change_it_in_prod"

    def init_db(self):
        connect_args = {"check_same_thread": False}
        return create_engine(self.DB_URL, echo=True, connect_args=connect_args)

    def get_inertia_config(self) -> InertiaConfig:
        return InertiaConfig(
            templates=self.get_templates(),
            manifest_json_path=self.MANIFEST_JSON,
            environment="development",
            use_flash_messages=True,
            use_flash_errors=True,
            entrypoint_filename="main.js",
            assets_prefix="/src",
        )
