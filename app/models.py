from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

########
# Post #
########


class PostBase(SQLModel):
    title: str
    content: str


class Post(PostBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    comments: list["Comment"] = Relationship(back_populates="post")
    created_at: datetime = Field(default=datetime.now(UTC))
    updated_at: datetime = Field(default=datetime.now(UTC))


class PostResponse(PostBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class CreatePost(PostBase):
    pass


###########
# Comment #
###########


class CommentBase(SQLModel):
    content: str


class Comment(CommentBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    post_id: UUID = Field(foreign_key="post.id")
    post: "Post" = Relationship(back_populates="comments")
    created_at: datetime = Field(default=datetime.now(UTC))
    updated_at: datetime = Field(default=datetime.now(UTC))


class CommentResponse(CommentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class CommentsResponse(SQLModel):
    comments: list[CommentResponse]


class CreateComment(CommentBase):
    pass


########
# Sync #
########


class SyncTable(SQLModel):
    created: list[dict] | None
    updated: list[dict] | None
    deleted: list[str] | None


class SyncTableResponse(SQLModel):
    changes: dict[str, SyncTable]
    timestamp: int | float


class PushSynchResponse(SQLModel):
    ok: bool


class GetSyncRequest(SQLModel):
    lastPulledAt: int | None
    schemaVersion: int
    migration: dict | None
