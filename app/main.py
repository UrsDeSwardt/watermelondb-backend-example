from typing import Any
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session
from app.db import get_db, engine
from app.models import PostResponse, CommentsResponse, SyncResponse
from app import crud

SQLModel.metadata.create_all(engine)

app = FastAPI()


# TODO: check return types


@app.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)) -> Any:
    return crud.get_post(session=db, post_id=post_id)


@app.get("/posts/{post_id}/comments", response_model=CommentsResponse)
def get_comments(post_id: int, db: Session = Depends(get_db)) -> Any:
    comments = crud.get_comments(session=db, post_id=post_id)
    return comments


@app.get("/sync", response_model=SyncResponse)
def get_sync() -> SyncResponse:
    return SyncResponse(status="synchronized")


@app.post("/sync", response_model=SyncResponse)
def push_sync() -> SyncResponse:
    return SyncResponse(status="sync pushed")
