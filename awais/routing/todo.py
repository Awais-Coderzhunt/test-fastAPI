from fastapi import APIRouter
from awais.models.todo import CreateTodo 


router = APIRouter(
    prefix="/todo",
    tags=["Todo"]
)

@router.get("")
def index():
    return {"message":"Todo"}

@router.post("")
@router.post("/")
def create_todo(item: CreateTodo):
    return {"message": item.model_dump()}
