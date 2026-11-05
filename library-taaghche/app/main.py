from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import create_db_and_tables
from app.routers import authors, books


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Taaghche Library", lifespan=lifespan)
app.include_router(authors.router)
app.include_router(books.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
