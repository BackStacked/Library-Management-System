from pydantic import BaseModel
from typing import Optional

# --------------------
# Book Schemas
# --------------------
class BookCreateSchema(BaseModel):
    title: str
    author: str
    isbn: str
  
class BookResponseSchema(BaseModel):
    id: str
    title: str
    author: str
    available: bool
