from functools import partial
from typing import Annotated

from fastapi import Depends, HTTPException

VALID_ORDERS = {"asc", "desc"}


def paginate(
    page: int = 1,
    size: int = 10,
    sort: str = "id",
    order: str = "asc",
    valid_sorts: set[str] | None = None,
) -> dict:
    if order not in VALID_ORDERS:
        raise HTTPException(status_code=422, detail=f"invalid order direction: {order}")
    if valid_sorts is not None and sort not in valid_sorts:
        raise HTTPException(status_code=422, detail=f"invalid sort field: {sort}")
    if page < 1:
        page = 1
    if size < 1:
        size = 1
    if size > 50:
        size = 50
    offset = (page - 1) * size
    return {
        "page": page,
        "size": size,
        "offset": offset,
        "sort": sort,
        "order": order,
    }


ProductPagination = Annotated[dict, Depends(partial(paginate, valid_sorts={"id", "name", "price"}))]
OrderPagination = Annotated[dict, Depends(partial(paginate, valid_sorts={"id", "user", "total"}))]
