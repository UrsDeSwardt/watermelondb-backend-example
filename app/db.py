from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.settings import settings

engine = create_engine(settings.DATABASE_URL)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
