# app/models/library.py

from app.database.db import users_collection, books_collection, borrowed_collection
from app.models.user import User
from app.models.book import Book
from typing import List, Optional

class LibraryDB:
    # User management
    async def add_user(self, user: User):
        await users_collection.insert_one(user.to_dict())
        return user

    async def get_user(self, user_id: str) -> Optional[User]:
        data = await users_collection.find_one({"id": user_id})
        if data:
            data.pop("_id", None)  # Remove MongoDB _id
            return User(**data)
        return None

    async def get_user_by_email(self, email: str) -> Optional[User]:
        data = await users_collection.find_one({"email": email.lower()})  # Ensure case-insensitive search
        if data:
            data.pop("_id", None)  # Remove MongoDB _id
            return User(**data)
        return None


    # Book management
    async def add_book(self, book: Book):
        await books_collection.insert_one(book.to_dict())
        return book

    async def get_book(self, book_id: str) -> Optional[Book]:
        data = await books_collection.find_one({"id": book_id})
        if data:
            data.pop("_id", None)  # remove Mongo’s ObjectId
            return Book(**data)
        return None

    async def list_books(self, skip: int = 0, limit: int = 10) -> List[Book]:
        cursor = books_collection.find().skip(skip).limit(limit)
        books = []
        async for b in cursor:
            b.pop("_id", None)  # only remove Mongo's internal id
            books.append(Book(**b))  # keep your own "id"
        return books


    # Borrow/Return
    async def borrow_book(self, user_id: str, book_id: str):
        book = await self.get_book(book_id)
        user = await self.get_user(user_id)
        if not book or not user:
            return None, "User or Book not found"

        # check borrowed
        borrowed = await borrowed_collection.find_one({"book_id": book_id})
        if borrowed:
            return None, "Book already borrowed"

        # mark as borrowed
        await books_collection.update_one(
            {"id": book_id},
            {"$set": {"is_borrowed": True}}
        )

        await borrowed_collection.insert_one({"user_id": user_id, "book_id": book_id})

        # refresh book state
        updated_book = await self.get_book(book_id)
        return updated_book, "Book borrowed successfully"


    async def return_book(self, user_id: str, book_id: str):
        borrowed = await borrowed_collection.find_one({"user_id": user_id, "book_id": book_id})
        if not borrowed:
            return None, "Book not borrowed"

        await borrowed_collection.delete_one({"user_id": user_id, "book_id": book_id})

        # mark as available
        await books_collection.update_one(
            {"id": book_id},
            {"$set": {"is_borrowed": False}}
        )

        return await self.get_book(book_id), "Book returned successfully"


    async def list_borrowed_books(self, user_id: str) -> List[Book]:
        cursor = borrowed_collection.find({"user_id": user_id})
        books = []
        async for record in cursor:
            book = await self.get_book(record["book_id"])
            if book:
                books.append(book)
        return books

        # Update book
    async def update_book(self, book_id: str, book: Book):
        await books_collection.update_one({"id": book_id}, {"$set": book.to_dict()})
        return book

    # Delete book
    async def delete_book(self, book_id: str):
        await books_collection.delete_one({"id": book_id})
