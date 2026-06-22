from fastapi import FastAPI, Depends
from typing import Annotated
from awais.models.query import QueryParams
from awais.routing.todo import router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


app = FastAPI()
app.include_router(router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
    status_code=400,
    content={
        "detail": exc.errors(), "body": exc.body
    }
    )

@app.get("/")
def root(query: Annotated[QueryParams, Depends()]):
    return {
        "message": "Awais Rasool ", "Params": query
    }


