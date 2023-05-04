from typing import Dict

from fastapi import FastAPI

from routes.author import author_router
from routes.book import book_router

app = FastAPI(openapi_url="/openapi.json", title="eBooks")


@app.get("/ping", tags=["Health"])
async def read_root() -> Dict:
    return {"message": "pong"}


app.router.prefix = "/api/v1"
app.include_router(author_router, prefix="/authors", tags=["Author"])
app.include_router(book_router, prefix="/books", tags=["Book"])
