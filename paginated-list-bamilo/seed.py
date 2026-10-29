from sqlmodel import Session, SQLModel

from db import engine
from models import Product

ROWS = [
    {"title": "Laptop", "category": "digital", "price": 50000},
    {"title": "Mouse", "category": "digital", "price": 1500},
    {"title": "Keyboard", "category": "digital", "price": 3000},
    {"title": "Monitor", "category": "digital", "price": 12000},
    {"title": "Novel", "category": "book", "price": 800},
    {"title": "Atlas", "category": "book", "price": 2500},
    {"title": "Comic", "category": "book", "price": 600},
    {"title": "Shirt", "category": "fashion", "price": 1800},
    {"title": "Shoes", "category": "fashion", "price": 4200},
    {"title": "Hat", "category": "fashion", "price": 900},
    {"title": "Lamp", "category": "home", "price": 2200},
    {"title": "Chair", "category": "home", "price": 7500},
]

SQLModel.metadata.create_all(engine)
with Session(engine) as session:
    for row in ROWS:
        session.add(
            Product(title=row["title"], category=row["category"], price=row["price"])
        )
    session.commit()
