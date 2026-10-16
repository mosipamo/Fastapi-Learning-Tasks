import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

_TMP_DIR = tempfile.mkdtemp(prefix="quera-mag-sample-")
os.environ["DATABASE_URL"] = "sqlite:///" + os.path.join(_TMP_DIR, "sample.db")

from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from database import engine
from main import app


class SampleTests(unittest.TestCase):
    def setUp(self):
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
        self.client = TestClient(app)

    def test_create_author_returns_201_and_an_id(self):
        """ساخت نویسندهٔ معتبر باید کد ۲۰۱ و یک شناسهٔ عددی برگرداند."""
        response = self.client.post("/authors", json={"name": "Ramtin"})
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.json().get("id"), int)

    def test_create_post_for_existing_author_returns_201(self):
        """ساخت پست برای نویسندهٔ موجود باید کد ۲۰۱ برگرداند."""
        author = self.client.post("/authors", json={"name": "Setareh"}).json()
        response = self.client.post(
            f"/authors/{author['id']}/posts",
            json={"title": "Hello", "content": "First post"},
        )
        self.assertEqual(response.status_code, 201)

    def test_get_author_returns_nested_posts(self):
        """پاسخ GET /authors/{id} باید فهرست پست‌های نویسنده را داشته باشد."""
        author = self.client.post("/authors", json={"name": "Parham"}).json()
        self.client.post(
            f"/authors/{author['id']}/posts",
            json={"title": "T1", "content": "C1"},
        )
        body = self.client.get(f"/authors/{author['id']}").json()
        self.assertEqual(len(body["posts"]), 1)
        self.assertEqual(body["posts"][0]["title"], "T1")


if __name__ == "__main__":
    unittest.main()
