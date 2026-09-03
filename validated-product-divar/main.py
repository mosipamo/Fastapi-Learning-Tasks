from fastapi import FastAPI

from models import ProductIn, ProductOut
from store import get_product, products, save_product

app = FastAPI(title="Divar Listings")


@app.get("/")
def read_root():
    return {"message": "Welcome to Divar Listings", "products_count": len(products)}


@app.post("/products", response_model=ProductOut)
def create_product(product: ProductIn):
    return save_product(product)


@app.get("/products/{product_id}", response_model=ProductOut)
def read_product(product_id: int):
    return get_product(product_id)
