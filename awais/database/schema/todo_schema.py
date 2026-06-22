from sqlalchemy import Boolean, Column, Integer, String

from ..db import Base

class TodoSchema(Base):
    __tablename__ = "todos"

    id=Column(Integer,primary_key=True , index=True , autoincrement=True)
    content= Column(String , nullable=False)
    is_completed = Column(Boolean , default=False , nullable=False)
