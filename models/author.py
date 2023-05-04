from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class Author(BaseModel):
    __tablename__ = "author"

    name = Column(String, index=True)
    books = relationship(
        "Book",
        back_populates="author",
        primaryjoin="and_(Author.id == Book.author_id, Book.is_active==True)"
    )
