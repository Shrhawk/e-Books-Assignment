from typing import List, Optional

from pydantic import BaseModel
from pydantic.datetime_parse import datetime

from schemas.book import BookSchema


class AuthorSchema(BaseModel):
    id: str
    name: str
    created_at: datetime
    updated_at: datetime
    books: List[BookSchema]

    class Config:
        orm_mode = True


class AuthorCreateRequest(BaseModel):
    name: str


class AuthorCreateResponse(BaseModel):
    id: str
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class AuthorUpdate(BaseModel):
    name: Optional[str] = None
