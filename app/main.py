
from fastapi import FastAPI
from app.database import Base, engine

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}
