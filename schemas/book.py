from pydantic import BaseModel
from typing import Optional

from pydantic.datetime_parse import datetime


class BookSchema(BaseModel):
    id: str
    name: str
    author_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class BookCreate(BaseModel):
    name: str
    author_id: str

    class Config:
        orm_mode = True


class BookUpdate(BaseModel):
    name: Optional[str] = None
    author_id: Optional[str] = None

    class Config:
        orm_mode = True
