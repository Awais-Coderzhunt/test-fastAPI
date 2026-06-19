
from fastapi import FastAPI
from awais.database import Base, engine
from awais.routes.TodoRoute import router as TodoRoute

app = FastAPI(title="Awais FastAPI")
Base.metadata.create_all(bind=engine)
app.include_router(TodoRoute)

@app.get("/" , tags=["main"])
def read_root():    
    return {"message": "Hello, World!"}
