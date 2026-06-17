from pydantic import BaseModel , Field
from typing import Union

class Todo(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=10, max_length=200)
    isComplete: Union[bool, None] = False