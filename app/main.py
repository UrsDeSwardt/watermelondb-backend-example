from typing import Any
from uuid import UUID

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from app import crud, sync
from app.db import create_db_and_tables, get_db
from app.models import (
    CommentResponse,
    CommentsResponse,
    CreateComment,
    CreatePost,
    PostResponse,
    PushSynchResponse,
    SyncTableResponse,
)

create_db_and_tables()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/posts", response_model=PostResponse)
async def create_post(post: CreatePost, db: Session = Depends(get_db)) -> PostResponse:
    created_post = crud.create_post(session=db, post=post)
    return PostResponse.model_validate(created_post)


@app.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: UUID, db: Session = Depends(get_db)) -> PostResponse:
    post = crud.get_post(session=db, post_id=post_id)
    return PostResponse.model_validate(post)


@app.post("/posts/{post_id}/comments", response_model=CommentResponse)
async def create_comment(
    post_id: UUID, comment: CreateComment, db: Session = Depends(get_db)
) -> CommentResponse:
    created_comment = crud.create_comment(session=db, post_id=post_id, comment=comment)
    return CommentResponse.model_validate(created_comment)


@app.get("/posts/{post_id}/comments", response_model=CommentsResponse)
async def get_comments(post_id: UUID, db: Session = Depends(get_db)) -> Any:
    comments = crud.get_comments(session=db, post_id=post_id)
    return CommentsResponse(comments=comments)


@app.get("/sync")
async def get_sync(
    last_pulled_at: float | None = None, db: Session = Depends(get_db)
) -> SyncTableResponse:
    result = sync.get_sync(last_pulled_at=last_pulled_at, session=db)
    return result


@app.post("/sync", response_model=PushSynchResponse)
async def push_sync(
    request: Request,
    # request_body: SyncTableRequest,
    db: Session = Depends(get_db),
) -> PushSynchResponse:
    changes = await request.json()
    return sync.push_sync(changes=changes, session=db)
