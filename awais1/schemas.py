
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, computed_field

from .image_utils import PROFILE_PICS_URL

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
    password: str = Field(min_length=1, max_length=255)

class UserUpdate(UserBase):
    userName: str | None = Field(default=None, min_length=1, max_length=100)
    email: str | None = Field(default=None, min_length=1, max_length=255)
    age: int | None = Field(default=None, ge=1, le=150)

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    profile_image: str | None = Field(default=None, exclude=True)

    @computed_field
    @property
    def profile_image_url(self) -> str | None:
        if not self.profile_image:
            return None
        return f"{PROFILE_PICS_URL}/{self.profile_image}"


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None
