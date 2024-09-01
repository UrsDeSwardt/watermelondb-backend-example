from sqlmodel import Session, select
from app.models import Post, Comment


def get_post(*, session: Session, post_id: int) -> Post | None:
    statement = select(Post).where(Post.id == post_id)
    post = session.exec(statement).first()
    return post


def get_comments(*, session: Session, post_id: int) -> list[Comment]:
    statement = select(Comment).where(Comment.post_id == post_id)
    comments = session.exec(statement).all()
    return list(comments)
