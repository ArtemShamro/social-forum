from pydantic import BaseModel
from typing import Optional

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
