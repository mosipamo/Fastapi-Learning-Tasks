from typing import Literal, Annotated

from fastapi import Depends, FastAPI, Query
from sqlmodel import Session
from contextlib import asynccontextmanager

import repository
from db import create_db_and_tables, get_session
from models import ProductPage

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="Bamilo Catalog", lifespan=lifespan)

@app.get("/products")
async def list_products(
    session: Session = Depends(get_session),
    category: str | None = None,
    min_price: int | None = Query(None, ge=0),
    max_price: int | None = Query(None, ge=0),
    sort: Annotated[Literal["price", "-price", "title", "-title", "id"], Query()] = "id",
    page: int | None = Query(ge=1, default=1),
    size: int | None = Query(ge=1, le=100, default=10),
) -> ProductPage:
    total, items = repository.list_products(
        session=session,
        category=category,
        min_price=min_price,
        max_price=max_price,
        sort=sort,
        page=page,
        size=size,
    )
    return ProductPage(
        total=total,
        page=page,
        size=size,
        items=items,
    )
