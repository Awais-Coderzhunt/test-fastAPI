
from pydantic import BaseModel

class QueryParams(BaseModel):
    name:str
    age:int

