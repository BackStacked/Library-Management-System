# app/models/book.py
import uuid
from typing import Optional

class Book:
    def __init__(
        self,
        title: str,
        author: str,
        isbn: str,
        id: Optional[str] = None,
        is_borrowed: bool = False
    ):
        self.id = id or str(uuid.uuid4())  # reuse from DB if provided
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = is_borrowed

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "is_borrowed": self.is_borrowed
        }
