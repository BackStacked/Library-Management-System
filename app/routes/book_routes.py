from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.book import Book
from app.models.library import LibraryDB
from app.schemas.book_schema import BookCreateSchema
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter()
library = LibraryDB()


# ------------------------
# CREATE (Admin only)
# ------------------------
@router.post("/", response_model=dict)
async def add_book(book: BookCreateSchema, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can add books")

    new_book = Book(title=book.title, author=book.author, isbn=book.isbn)
    await library.add_book(new_book)
    return new_book.to_dict()


# ------------------------
# READ (Everyone)
# ------------------------
@router.get("/", response_model=List[dict])
async def list_books(skip: int = 0, limit: int = 10):
    books = await library.list_books(skip=skip, limit=limit)
    return [b.to_dict() for b in books]


@router.get("/{book_id}", response_model=dict)
async def get_book(book_id: str):
    book = await library.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.to_dict()


# ------------------------
# UPDATE (Admin only)
# ------------------------
@router.put("/{book_id}", response_model=dict)
async def update_book(book_id: str, book: BookCreateSchema, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update books")

    existing_book = await library.get_book(book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")

    # update fields
    updated_data = existing_book.to_dict()
    updated_data.update(book.dict())
    updated_book = Book(**updated_data)

    # save in DB
    await library.update_book(book_id, updated_book)
    return updated_book.to_dict()


# ------------------------
# DELETE (Admin only)
# ------------------------
@router.delete("/{book_id}", response_model=dict)
async def delete_book(book_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete books")

    existing_book = await library.get_book(book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")

    await library.delete_book(book_id)
    return {"message": "Book deleted successfully", "id": book_id}
