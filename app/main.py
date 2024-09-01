from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlmodel import SQLModel
from app.db import get_db, engine
from app.models import Post, Comment, PostResponse, CommentResponse, SyncResponse

SQLModel.metadata.create_all(engine)

app = FastAPI()


@app.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        return {"error": "Post not found"}
    return PostResponse.model_validate(post)


@app.get("/posts/{post_id}/comments", response_model=CommentsResponse)
def get_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return CommentsResponse(
        comments=[
            CommentResponse(
                id=comment.id, content=comment.content, post_id=comment.post_id
            )
            for comment in comments
        ]
    )


@app.get("/sync", response_model=SyncResponse)
def get_sync():
    return SyncResponse(status="synchronized")


@app.post("/sync", response_model=SyncResponse)
def push_sync():
    return SyncResponse(status="sync pushed")
