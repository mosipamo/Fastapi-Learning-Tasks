products: dict[int, dict] = {}
_next_id = 0


def save_product(data: dict) -> dict:
    global _next_id
    product_id = _next_id
    _next_id += 1
    products[product_id] = data
    return {"id": product_id, **data.model_dump()}


def get_product(product_id: int) -> dict | None:
    product = products.get(product_id)
    if product:
        return {"id": product_id, **product.model_dump()}
    return None
