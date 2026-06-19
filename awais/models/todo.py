from pydantic import BaseModel, Field

class CreateTodo(BaseModel):
    contend: str = Field(..., max_length=500, min_length=3)
    is_completed: bool = False
