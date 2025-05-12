from pydantic import BaseModel
from typing import Optional
from typing import Literal


class CreatePostRequest(BaseModel):
    title: str
    description: str
    private: bool


class DeletePostRequest(BaseModel):
    post_id: str


class GetPostRequest(BaseModel):
    post_id: str


class UpdatePostRequest(BaseModel):
    post_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    private: Optional[bool] = None


class CreateCommentRequest(BaseModel):
    post_id: int
    comment: str


class GetCountRequest(BaseModel):
    post_id: int
    target_type: Literal["like", "view", "comment"]


class GetDynamicsRequest(BaseModel):
    post_id: int
    target_type: Literal["like", "view", "comment"]


class GetTopPostsRequest(BaseModel):
    target_type: Literal["like", "view", "comment"]
    limit: int = 10


class GetTopUsersRequest(BaseModel):
    target_type: Literal["like", "view", "comment"]
    limit: int = 10
