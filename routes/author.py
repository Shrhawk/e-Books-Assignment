from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload, Session

from database.db import get_db
from models import Author
from schemas.author import AuthorSchema, AuthorCreateRequest, AuthorCreateResponse, AuthorUpdate

author_router = APIRouter()


@author_router.post("", response_model=AuthorCreateResponse)
async def create_author(author_name: str, db: Session = Depends(get_db)) -> AuthorCreateRequest:
    """Create a new author in the author table"""
    author = Author(name=author_name)
    db.add(author)
    await db.commit()
    await db.refresh(author)
    return author


@author_router.get("/{author_id}", response_model=AuthorSchema)
async def get_author(author_id: str, db: Session = Depends(get_db)) -> AuthorSchema:
    """Retrieve an author with the specified ID from the author table"""
    query = select(Author).options(selectinload(Author.books)).where(Author.id == author_id, Author.is_active)
    author = await db.execute(query)
    author = author.scalars().one_or_none()
    if author is None:
        raise HTTPException(status_code=422, detail="Author not found")
    return author


@author_router.get("", response_model=List[AuthorSchema])
async def get_authors(db: Session = Depends(get_db)) -> List[AuthorSchema]:
    """Retrieve all authors from the author table"""
    query = select(Author).options(selectinload(Author.books)).where(Author.is_active)
    result = await db.execute(query)
    authors = result.scalars().all()
    return authors


@author_router.patch("/{author_id}", response_model=AuthorSchema)
async def update_order(author_id: str, author_obj: AuthorUpdate, db: Session = Depends(get_db)) -> AuthorSchema:
    """Delete an author with the specified ID from the author table"""
    query = select(Author).options(selectinload(Author.books)).where(Author.id == author_id, Author.is_active)
    result = await db.execute(query)
    author = result.scalars().one_or_none()
    if not author:
        raise HTTPException(status_code=422, detail="Author not found")
    author.name = author_obj.name
    await db.commit()
    return author


@author_router.delete("/{author_id}", response_model=dict)
async def delete_author(author_id: str, db: Session = Depends(get_db)) -> dict:
    """Delete an author with the specified ID from the aSessionuthor table"""
    author = await db.execute(select(Author).where(Author.id == author_id, Author.is_active))
    author = author.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=422, detail="Author not found")
    author.is_active = False
    await db.commit()
    return {"detail": "Author deleted successfully"}
