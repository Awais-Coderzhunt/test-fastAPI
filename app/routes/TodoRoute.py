
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/v1", tags=["todos"])

@router.post("/create")
async def create_todo(todo: dict):
    return todo