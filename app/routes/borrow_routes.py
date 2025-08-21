from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.library import LibraryDB
from app.utils.auth import get_current_user
from app.schemas.book_schema import BookResponseSchema

router = APIRouter()
library = LibraryDB()

@router.post("/borrow/{book_id}", response_model=dict)
async def borrow_book(book_id: str, current_user=Depends(get_current_user)):
    book, msg = await library.borrow_book(current_user.id, book_id)
    if not book:
        raise HTTPException(status_code=400, detail=msg)
    return book.to_dict()

@router.post("/return/{book_id}", response_model=dict)
async def return_book(book_id: str, current_user=Depends(get_current_user)):
    book, msg = await library.return_book(current_user.id, book_id)
    if not book:
        raise HTTPException(status_code=400, detail=msg)
    return book.to_dict()

@router.get("/mybooks", response_model=List[dict])
async def list_my_books(current_user=Depends(get_current_user)):
    books = await library.list_borrowed_books(current_user.id)
    return [b.to_dict() for b in books]
