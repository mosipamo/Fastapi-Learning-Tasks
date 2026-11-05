import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

import app.db as db_module
from app.main import app


class SampleTests(unittest.TestCase):
    """چند تست نمونه برای آزمودن سریع پروژه روی پایگاه دادهٔ تازه."""

    def setUp(self):
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        SQLModel.metadata.create_all(self.engine)

        def override_get_session():
            with Session(self.engine) as session:
                yield session

        app.dependency_overrides[db_module.get_session] = override_get_session
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()
        SQLModel.metadata.drop_all(self.engine)
        self.engine.dispose()

    def test_create_and_read_author(self):
        res = self.client.post("/authors", json={"name": "Sadegh Hedayat", "country": "Iran"})
        self.assertEqual(res.status_code, 201)
        aid = res.json()["id"]
        got = self.client.get(f"/authors/{aid}")
        self.assertEqual(got.status_code, 200)
        self.assertEqual(got.json()["name"], "Sadegh Hedayat")

    def test_create_book_for_author_and_list(self):
        aid = self.client.post("/authors", json={"name": "A", "country": "Iran"}).json()["id"]
        res = self.client.post(
            "/books",
            json={"title": "Buf-e Kur", "year": 1936, "price": 45000, "author_id": aid},
        )
        self.assertEqual(res.status_code, 201)
        body = self.client.get("/books").json()
        self.assertEqual(body["total"], 1)

    def test_author_with_books_relationship(self):
        aid = self.client.post("/authors", json={"name": "A", "country": "Iran"}).json()["id"]
        self.client.post(
            "/books",
            json={"title": "B1", "year": 2000, "price": 1000, "author_id": aid},
        )
        body = self.client.get(f"/authors/{aid}/books").json()
        self.assertEqual(len(body["books"]), 1)


if __name__ == "__main__":
    unittest.main()
