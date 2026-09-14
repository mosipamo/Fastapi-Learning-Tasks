from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException

from menu_resource import MENU, Connection, get_connection

API_KEY = "snappfood-internal"


def require_api_key(x_api_key: Annotated[str | None, Header()] = None) -> None:
    if x_api_key is None or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="invalid api key")

app = FastAPI(title="SnappFood Menu API", dependencies=[Depends(require_api_key)])

Conn = Annotated[Connection, Depends(get_connection)]


@app.get("/")
def welcome() -> dict:
    return {"message": "SnappFood menu API"}


@app.get("/menu")
def list_menu(conn: Conn, page: int = 1, size: int = 10) -> dict:
    if page < 1:
        page = 1
    if size < 1:
        size = 1
    if size > 50:
        size = 50
    offset = (page - 1) * size
    items = conn.fetch_page(offset, size)
    total = len(MENU)
    return {"page": page, "size": size, "total": total, "items": items}


@app.get("/menu/{item_id}")
def get_menu_item(item_id: int, conn: Conn) -> dict:
    item = conn.fetch_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="item not found")
    return item
