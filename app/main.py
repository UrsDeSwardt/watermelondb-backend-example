from typing import Any

from fastapi import Depends, FastAPI
from sqlmodel import Session

from app import crud, sync
from app.db import create_db_and_tables, get_db
from app.models import (CommentResponse, CommentsResponse, CreateComment,
                        CreatePost, PostResponse, SyncTable, SyncTableResponse)

create_db_and_tables()

app = FastAPI()


# TODO: check return types


@app.post("/posts", response_model=PostResponse)
def create_post(post: CreatePost, db: Session = Depends(get_db)) -> Any:
    return crud.create_post(session=db, post=post)


@app.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)) -> Any:
    return crud.get_post(session=db, post_id=post_id)


@app.post("/posts/{post_id}/comments", response_model=CommentResponse)
def create_comment(
    post_id: int, comment: CreateComment, db: Session = Depends(get_db)
) -> Any:
    return crud.create_comment(session=db, post_id=post_id, comment=comment)


@app.get("/posts/{post_id}/comments", response_model=CommentsResponse)
def get_comments(post_id: int, db: Session = Depends(get_db)) -> Any:
    comments = crud.get_comments(session=db, post_id=post_id)
    return CommentsResponse(comments=comments)


@app.get("/sync", response_model=SyncTableResponse)
def get_sync(
    last_pulled_at: float | None = None, db: Session = Depends(get_db)
) -> SyncTableResponse:
    return sync.get_sync(last_pulled_at=last_pulled_at, session=db)


@app.post("/sync", response_model=list[SyncTable])
def push_sync() -> list[SyncTable]:
    return [SyncTable(created=[], updated=[], deleted=[])]
