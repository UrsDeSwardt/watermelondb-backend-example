from typing import Generator
from sqlmodel import Session, create_engine, SQLModel

DATABASE_URL = "postgresql://user:password@localhost/dbname"  # Update with your PostgreSQL credentials

engine = create_engine(DATABASE_URL)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
