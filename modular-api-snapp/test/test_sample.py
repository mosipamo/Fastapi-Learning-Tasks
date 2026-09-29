import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class SampleTests(unittest.TestCase):
    def test_welcome_endpoint_returns_status_code_200_on_root_path(self):
        """مسیر / باید با کد ۲۰۰ و یک شیء JSON پاسخ دهد."""
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)

    def test_users_list_endpoint_returns_all_eight_users(self):
        """مسیر /users باید هر هشت کاربر را برگرداند."""
        body = client.get("/users").json()
        self.assertEqual(len(body), 8)
        self.assertEqual([u["id"] for u in body], [1, 2, 3, 4, 5, 6, 7, 8])

    def test_user_detail_endpoint_missing_user_returns_404(self):
        """کاربر ناموجود باید کد ۴۰۴ بدهد."""
        self.assertEqual(client.get("/users/999").status_code, 404)

    def test_rides_list_endpoint_filters_by_completed_status(self):
        """با status=completed باید سه سفر پایان‌یافته برگردند."""
        body = client.get("/rides", params={"status": "completed"}).json()
        self.assertEqual([r["id"] for r in body], [101, 104, 106])

    def test_openapi_includes_users_and_rides_tags(self):
        """برچسب‌های users و rides باید در سند OpenAPI باشند."""
        spec = client.get("/openapi.json").json()
        tags = {t for p in spec["paths"].values() for m in p.values() for t in m.get("tags", [])}
        self.assertIn("users", tags)
        self.assertIn("rides", tags)


if __name__ == "__main__":
    unittest.main()
