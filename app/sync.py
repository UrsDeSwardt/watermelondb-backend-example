from datetime import UTC, datetime

from sqlmodel import Session, select

from app.models import (
    Comment,
    Post,
    PushSynchResponse,
    SyncTableResponse,
)


def get_sync(*, last_pulled_at: float | None, session: Session) -> SyncTableResponse:
    last_pull = datetime.fromtimestamp(last_pulled_at or 0.0, UTC)

    posts = session.exec(select(Post).where(Post.updated_at > last_pull)).all()

    comments = session.exec(select(Comment).where(Comment.updated_at > last_pull)).all()

    return SyncTableResponse(
        changes={
            "post": {
                "created": [p.model_dump(mode="json") for p in posts],
                "updated": [],
                "deleted": [],
            },
            "comment": {
                "created": [c.model_dump(mode="json") for c in comments],
                "updated": [],
                "deleted": [],
            },
        },
        timestamp=datetime.now().timestamp(),
    )


def push_sync(*, changes: dict, session: Session) -> PushSynchResponse:
    posts = changes.get("post")
    comments = changes.get("comment")

    if posts:
        for post in posts.get("created") or {}:
            session.add(Post.model_validate(post))

    if comments:
        for comment in comments.get("created") or {}:
            session.add(Comment.model_validate(comment))

    session.commit()

    return PushSynchResponse(ok=True)
