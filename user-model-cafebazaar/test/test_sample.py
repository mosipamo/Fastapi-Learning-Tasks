import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

_TMP_DIR = tempfile.mkdtemp(prefix="quera-bazaar-sample-")
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

    def test_create_user_returns_201_and_an_id(self):
        """ساخت کاربر معتبر باید کد ۲۰۱ و یک شناسهٔ عددی برگرداند."""
        response = self.client.post(
            "/users", json={"username": "nazanin", "email": "nazanin@bazaar.ir"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.json().get("id"), int)

    def test_get_user_by_id_returns_the_created_user(self):
        """کاربر ساخته‌شده باید با شناسه‌اش قابل خواندن باشد."""
        created = self.client.post(
            "/users", json={"username": "peyman", "email": "peyman@bazaar.ir"}
        ).json()
        body = self.client.get(f"/users/{created['id']}").json()
        self.assertEqual(body["username"], "peyman")

    def test_list_users_returns_created_users(self):
        """فهرست کاربران باید کاربران ساخته‌شده را برگرداند."""
        self.client.post("/users", json={"username": "a1", "email": "a1@bazaar.ir"})
        self.client.post("/users", json={"username": "a2", "email": "a2@bazaar.ir"})
        body = self.client.get("/users").json()
        self.assertEqual(len(body), 2)


if __name__ == "__main__":
    unittest.main()
