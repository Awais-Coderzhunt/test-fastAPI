from fastapi import FastAPI

from app.database import Base, engine
from app.models.userModels import User
from app.routers.users import router as user
from app.routers.auth import router as auth

app = FastAPI(title="Authentication API")

# Base.metadata.create_all(bind=engine)

app.include_router(user)
app.include_router(auth)



@app.get("/")
def read_root():
    return {"message": "Authentication API is running"}
