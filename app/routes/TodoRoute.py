
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.Todomodel import TodoTable
from app.schemas.TodoSchema import TodoCreate, TodoResponse

router = APIRouter(prefix="/api", tags=["todos"])


@router.post("/create", response_model=TodoResponse)
async def create_todo(data: TodoCreate, db: Session = Depends(get_db)):
    todo = TodoTable(
        title=data.title,
        description=data.description,
        isComplete=data.isComplete,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@router.get("/", response_model=list[TodoResponse])
async def get_todos(db: Session = Depends(get_db)):
    return db.query(TodoTable).all()

@router.get("/{id}", response_model=TodoResponse)
async def get_todoById(id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoTable).filter(TodoTable.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.delete("/delete/{id}")
async def delete_todoById(id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoTable).filter(TodoTable.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}
