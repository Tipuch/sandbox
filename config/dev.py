from sqlalchemy import create_engine

from .config import Config


class DevConfig(Config):
    sqlite_file_name = "database.db"
    DB_URL = f"sqlite:///{sqlite_file_name}"

    def init_db(self):
        connect_args = {"check_same_thread": False}
        return create_engine(self.DB_URL, echo=True, connect_args=connect_args)
