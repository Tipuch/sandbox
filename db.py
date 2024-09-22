from sqlmodel import SQLModel, Session
from main import config

engine = config.init_db()


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
