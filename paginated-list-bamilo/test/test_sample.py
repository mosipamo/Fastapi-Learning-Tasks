import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

import db as db_module
from main import app
from models import Product

SEED = [
    {"title": "Laptop", "category": "digital", "price": 50000},
    {"title": "Mouse", "category": "digital", "price": 1500},
    {"title": "Novel", "category": "book", "price": 800},
]


class CatalogSampleTest(unittest.TestCase):
    """چند تست نمونهٔ مسیر اصلی برای محک‌زدن سریع پیاده‌سازی."""

    def setUp(self):
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        SQLModel.metadata.create_all(self.engine)
        with Session(self.engine) as session:
            for row in SEED:
                session.add(Product(**row))
            session.commit()

        def override_get_session():
            with Session(self.engine) as session:
                yield session

        app.dependency_overrides[db_module.get_session] = override_get_session
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()
        SQLModel.metadata.drop_all(self.engine)
        self.engine.dispose()

    def test_envelope_total(self):
        """total باید برابر تعداد کل محصولات باشد."""
        self.assertEqual(self.client.get("/products").json()["total"], 3)

    def test_filter_category(self):
        """فیلتر دسته باید فقط محصولات همان دسته را بدهد."""
        body = self.client.get("/products", params={"category": "digital"}).json()
        self.assertEqual(body["total"], 2)

    def test_sort_price_ascending(self):
        """sort=price باید از ارزان به گران مرتب کند."""
        prices = [
            i["price"]
            for i in self.client.get("/products", params={"sort": "price"}).json()["items"]
        ]
        self.assertEqual(prices, sorted(prices))


if __name__ == "__main__":
    unittest.main()
