from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class Book(BaseModel):
    __tablename__ = "book"

    name = Column(String, index=True)
    author_id = Column(String, ForeignKey("author.id"))
    author = relationship("Author", back_populates="books")
