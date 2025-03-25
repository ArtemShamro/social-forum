from pydantic import BaseModel

class PostCreateRequest(BaseModel):
    # owner_id: int
    title: str
    description: str
    private: bool