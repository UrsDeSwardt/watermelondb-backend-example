from uuid import UUID
from sqlmodel import Session, select

from app.models import Comment, CreateComment, CreatePost, Post


def create_post(*, session: Session, post: CreatePost) -> Post:
    db_post = Post.model_validate(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


def get_post(*, session: Session, post_id: UUID) -> Post | None:
    statement = select(Post).where(Post.id == post_id)
    post = session.exec(statement).first()
    return post


def create_comment(
    *, session: Session, post_id: UUID, comment: CreateComment
) -> Comment:
    db_comment = Comment.model_validate(
        comment,
        update={"post_id": post_id},
    )

    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)
    return db_comment


def get_comments(*, session: Session, post_id: UUID) -> list[Comment]:
    statement = select(Comment).where(Comment.post_id == post_id)
    comments = session.exec(statement).all()
    return list(comments)
