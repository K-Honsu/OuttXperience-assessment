from pydantic import BaseModel, constr
from typing import Optional


class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    isbn: str


class BookUpdate(BaseModel):
    title: str
    author: str
    year: int
    isbn: str

    """
    fastapi==0.111.0
fastapi-cli==0.0.2
uvicorn==0.29.0


    """
# postgresql://postgres:Anjola123@@localhost:5432/fastapi-assessment