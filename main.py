
from fastapi import FastAPI , Depends
from typing import Annotated
from test import QueryParams 
app = FastAPI()

@app.get("/")
def root(query: Annotated[QueryParams , Depends()]):
    
    return {
        "message": "Awais Rasool ", "Params": query
    }

