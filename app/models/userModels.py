from sqlalchemy import Column, Integer, String

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    userName = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    password = Column(String, nullable=False)
