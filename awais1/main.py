from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routing.post import router as post_router
from .routing.user import router as user_router
from .routing.auth import router as auth_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="awais1/static"), name="static")
app.include_router(post_router)
app.include_router(user_router)
app.include_router(auth_router)
