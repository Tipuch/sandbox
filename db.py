from sqlmodel import SQLModel, Session
from config.config import settings

engine = settings.init_db()


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
