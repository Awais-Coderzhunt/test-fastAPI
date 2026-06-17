
from fastapi import FastAPI
from app.routes.TodoRoute import router as TodoRoute

app = FastAPI(title="Awais FastAPI")
app.include_router(TodoRoute)

@app.get("/" , tags=["main"])
def read_root():    
    return {"message": "Hello, World!"}
