import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class SampleTests(unittest.TestCase):
    def test_welcome_endpoint_returns_status_code_200_on_root_path(self):
        """مسیر / باید با کد ۲۰۰ و کلید movies_count برابر ۴ پاسخ دهد."""
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["movies_count"], 4)

    def test_get_movie_returns_status_code_404_for_missing_movie(self):
        """فیلم ناموجود باید کد ۴۰۴ با کلید detail بدهد."""
        response = client.get("/movies/9999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.json())

    def test_play_premium_movie_by_free_user_returns_403(self):
        """کاربر رایگان روی فیلم ویژه باید کد ۴۰۳ بگیرد."""
        response = client.get("/movies/11/play", params={"user_id": 3})
        self.assertEqual(response.status_code, 403)

    def test_age_restricted_play_uses_structured_error_body(self):
        """محدودیت سنی باید پاسخ ساختارمند با کلید error و code برابر age_restricted بدهد."""
        body = client.get("/movies/12/play", params={"user_id": 4}).json()
        self.assertEqual(body["error"]["code"], "age_restricted")


if __name__ == "__main__":
    unittest.main()
