from sqlmodel import Session

from models import Product


def list_products(
    session: Session,
    *,
    category: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    sort: str | None = None,
    page: int = 1,
    size: int = 10,
) -> tuple[int, list[Product]]:

    query = session.query(Product)
    if category:
        query = query.filter(Product.category == category)
    if min_price:
        query = query.filter(Product.price >= min_price)
    if max_price:
        query = query.filter(Product.price <= max_price)
    if sort:
        if sort.startswith("-"):
            sort = sort[1:]
            ascending = False
        else:
            ascending = True
        query = query.order_by(Product.__dict__[sort].asc() if ascending else Product.__dict__[sort].desc())
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return total, items
