from sqlmodel import Field, Relationship, SQLModel

########
# Post #
########


class PostBase(SQLModel):
    title: str
    content: str


class Post(PostBase, table=True):
    id: int = Field(default=None, primary_key=True)
    comments: list["Comment"] = Relationship(back_populates="post")


class PostResponse(PostBase):
    id: int


class CreatePost(PostBase):
    pass


###########
# Comment #
###########


class CommentBase(SQLModel):
    content: str


class Comment(CommentBase, table=True):
    id: int = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="posts.id")
    post: "Post" = Relationship(back_populates="comments")


class CommentResponse(CommentBase):
    id: int


class CommentsResponse(SQLModel):
    comments: list[CommentResponse]


class CreateComment(CommentBase):
    pass


########
# Sync #
########


class SyncResponse(SQLModel):
    status: str
