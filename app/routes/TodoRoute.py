
from fastapi import APIRouter, Depends
from app.models.Todomodel import Todo

router = APIRouter(prefix="/api", tags=["todos"])


todos = []

@router.post("/create")
async def create_todo(data: Todo):

    new_data = dict(data)
    new_data["id"] = len(todos) + 1

    todos.append(new_data)
    return {
        "msg": data
    }

@router.get("/")
async def get_todos():
    return {
        "msg": todos
    }

@router.get("/{id}")
async def get_todoById(id: int):
    for todo in todos:
        if todo["id"] == id:
            return {
                "msg": todo
            }
    return {
        "msg": "Todo not found"
    }