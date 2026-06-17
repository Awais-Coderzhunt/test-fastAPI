from pydantic import BaseModel, ConfigDict, Field


class TodoCreate(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=10, max_length=200)
    isComplete: bool = False


class TodoUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, min_length=10, max_length=200)
    isComplete: bool | None = None


class TodoResponse(TodoCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
