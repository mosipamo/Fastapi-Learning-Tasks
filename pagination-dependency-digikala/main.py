from fastapi import FastAPI

from data import ORDERS, PRODUCTS
from deps import OrderPagination, ProductPagination

app = FastAPI(title="Digikala Listing API")


@app.get("/")
async def welcome():
    return {
        "message": "Digikala listing API",
        "products_count": len(PRODUCTS),
        "orders_count": len(ORDERS),
    }


@app.get("/products")
def list_products(
    pagination: ProductPagination,
    min_price: int | None = None,
) -> dict:
    if min_price:
        filtered_products = [p for p in PRODUCTS if p["price"] >= min_price]
    else:
        filtered_products = PRODUCTS
    sorted_products = sorted(filtered_products, key=lambda p: p[pagination["sort"]], reverse=(pagination["order"] == "desc"))
    return {
        "page": pagination["page"],
        "size": pagination["size"],
        "sort": pagination["sort"],
        "order": pagination["order"],
        "total": len(sorted_products),
        "items": sorted_products[pagination["offset"]:pagination["offset"] + pagination["size"]],
    }


@app.get("/orders")
def list_orders(
    pagination: OrderPagination,
    min_total: int | None = None,
) -> dict:
    if min_total:
        filtered_orders = [o for o in ORDERS if o["total"] >= min_total]
    else:
        filtered_orders = ORDERS
    sorted_orders = sorted(filtered_orders, key=lambda o: o[pagination["sort"]], reverse=(pagination["order"] == "desc"))
    return {
        "page": pagination["page"],
        "size": pagination["size"],
        "sort": pagination["sort"],
        "order": pagination["order"],
        "total": len(sorted_orders),
        "items": sorted_orders[pagination["offset"]:pagination["offset"] + pagination["size"]],
    }
