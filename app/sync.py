from datetime import datetime

from sqlmodel import Session, select

from app.models import Comment, Post, SyncTableResponse


def get_sync(*, session: Session) -> SyncTableResponse:
    posts = session.exec(select(Post)).all()
    comments = session.exec(select(Comment)).all()
    return SyncTableResponse(
        changes={
            "post": {
                "created": posts,
                "updated": [],
                "deleted": [],
            },
            "comment": {
                "created": comments,
                "updated": [],
                "deleted": [],
            },
        },
        timestamp=datetime.now().timestamp(),
    )
