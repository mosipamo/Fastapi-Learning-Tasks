from fastapi import FastAPI

from data import products
from search import search_products

app = FastAPI(title="Snapp Market Product Search")


@app.get("/")
def welcome():
    return {"message": "Snapp Market product search", "products_count": len(products)}


@app.get("/products")
def search(q: str = None, category: str = None, page: int = 1, page_size: int = 10):
    return search_products(products, q, category, page, page_size)
