import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

import db as db_module
from main import app


class NotesSampleTest(unittest.TestCase):
    """چند تست نمونهٔ مسیر اصلی برای محک‌زدن سریع پیاده‌سازی."""

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

    def test_create_note_returns_201(self):
        """ساخت یادداشت باید کد ۲۰۱ بازگرداند."""
        res = self.client.post("/notes", json={"title": "سلام", "content": "دنیا"})
        self.assertEqual(res.status_code, 201)

    def test_create_note_rejects_empty_title(self):
        """عنوان خالی باید با کد ۴۲۲ رد شود."""
        res = self.client.post("/notes", json={"title": "", "content": "دنیا"})
        self.assertEqual(res.status_code, 422)

    def test_list_notes_empty_at_first(self):
        """فهرست اولیه باید خالی باشد."""
        self.assertEqual(self.client.get("/notes").json(), [])

    def test_list_notes_search_filters(self):
        """جست‌وجوی q باید فهرست را محدود کند."""
        self.client.post("/notes", json={"title": "خرید کتاب", "content": "x"})
        self.client.post("/notes", json={"title": "تماشای فیلم", "content": "y"})
        body = self.client.get("/notes", params={"q": "کتاب"}).json()
        self.assertEqual([n["title"] for n in body], ["خرید کتاب"])

    def test_read_missing_note_is_404(self):
        """خواندن یادداشت ناموجود باید ۴۰۴ بدهد."""
        self.assertEqual(self.client.get("/notes/1").status_code, 404)


if __name__ == "__main__":
    unittest.main()
