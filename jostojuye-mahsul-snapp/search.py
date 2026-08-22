def search_products(
    products: list[dict],
    q: str | None = None,
    category: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> dict:

    if q:
        products = [p for p in products if q.lower() in p["name"].lower()]
    if category:
        products = [p for p in products if p["category"] == category]

    total = len(products)
    if page_size:
        products = products[(page - 1) * page_size : page * page_size]

    return {"total": total, "page": page, "page_size": page_size, "items": products}
