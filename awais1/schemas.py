
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_posted: datetime


class UserBase(BaseModel):
    userName: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=255)
    age: int = Field(ge=1, le=150)


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
