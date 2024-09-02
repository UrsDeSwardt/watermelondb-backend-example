from sqlmodel import Session, delete

from app.db import create_db_and_tables, engine
from app.models import Comment, Post


def clear_db() -> None:
    create_db_and_tables()

    with Session(engine) as session:
        session.execute(delete(Comment))
        session.execute(delete(Post))
        session.commit()
