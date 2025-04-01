from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional


class CreatePost(BaseModel):
    owner_id: Optional[str] = Field(None, min_length=1, max_length=50, description="Owner_ID, от 1 до 50 символов")
    title: Optional[str] = Field(None, min_length=1, max_length=10000, description="Название, от 1 до 10000 символов")
    description: Optional[str] = Field(None, min_length=1, max_length=50, description="Описание, от 1 до 50 символов")
    private: Optional[bool] = Field(False, description="Приватность поста")
    
    model_config = ConfigDict(from_attributes=True)


class GetPost(BaseModel):
    post_id: str = Field(..., min_length=1, max_length=50, description="Post_ID, от 1 до 50 символов")
    owner_id: str = Field(..., min_length=1, max_length=50, description="Owner_ID, от 1 до 50 символов")


class ListPosts(BaseModel):
    owner_id: str = Field(..., min_length=1, max_length=50, description="ID, от 1 до 50 символов")
    page: int = Field(1, description="Номер страницы")
    per_page: int = Field(10, description="Количество записей на странице")


class UpdatePost(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=50, description="Название, от 1 до 50 символов")
    description: Optional[str] = Field(None, min_length=1, max_length=10000, description="Описание, от 1 до 10000 символов")
    private: Optional[bool] = Field(None, description="Приватность поста")

    @field_validator('*', mode='before')
    def empty_str_to_none(cls, v):
        if isinstance(v, str) and v.strip() == "":
            return None
        return v