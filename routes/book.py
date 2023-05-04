from typing import List

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload, Session

from database.db import get_db
from models import Author
from models.book import Book
from schemas.book import BookCreate, BookUpdate, BookSchema

book_router = APIRouter()


@book_router.get("", response_model=List[BookSchema])
async def get_books(db: Session = Depends(get_db)) -> List[BookSchema]:
    """Retrieve all books from the book table"""
    query = select(Book).options(selectinload(Book.author)).where(Book.is_active)
    result = await db.execute(query)
    books = result.scalars().all()
    return books


@book_router.get("/{book_id}", response_model=BookSchema)
async def get_book(book_id: str, db: Session = Depends(get_db)) -> BookSchema:
    """Retrieve a book with the specified ID from the book table"""
    book = await db.execute(select(Book).where(Book.id == book_id, Book.is_active))
    book = book.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=422, detail="Book not found")
    return book


@book_router.post("", response_model=BookSchema)
async def create_book(book: BookCreate, db: Session = Depends(get_db)) -> BookSchema:
    """Create a new book in the book table"""
    book = Book(name=book.name, author_id=book.author_id)
    db.add(book)
    await db.commit()
    return book


@book_router.patch("/{book_id}", response_model=BookSchema)
async def update_book(book_id: str, updated_book: BookUpdate, db: Session = Depends(get_db)) -> BookSchema:
    """Update book's name or author ID with the specified ID from the book table"""
    book = await db.execute(select(Book).where(Book.id == book_id, Book.is_active))
    book = book.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=422, detail="Book not found")
    author = await db.execute(select(Author).where(Author.id == updated_book.author_id, Author.is_active))
    author = author.scalar_one_or_none()
    if author:
        book.author_id = updated_book.author_id
    book.name = updated_book.name
    await db.commit()
    return book


@book_router.delete("/{book_id}", response_model=dict)
async def delete_book(book_id: str, db: Session = Depends(get_db)) -> dict:
    """Delete a book with the specified ID from the book table"""
    book = await db.execute(select(Book).where(Book.id == book_id, Book.is_active))
    book = book.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=422, detail="Book not found")
    book.is_active = False
    await db.commit()
    return {"detail": "Book deleted successfully"}
