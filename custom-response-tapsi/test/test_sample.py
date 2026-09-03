import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class SampleTests(unittest.TestCase):
    def test_welcome_endpoint_returns_status_code_200_on_root_path(self):
        """مسیر / باید کد ۲۰۰ بدهد و rides_count آن با تعداد سفرهای /rides بخواند."""
        c = TestClient(app)
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        listed = c.get("/rides").json()["rides"]
        # متن پیام خوش‌آمدگویی دلخواه است؛ فقط شمارش سفرها سنجیده می‌شود.
        self.assertEqual(response.json()["rides_count"], len(listed))

    def test_create_ride_returns_status_code_201_created(self):
        """ساخت سفر باید کد ۲۰۱ و سربرگ‌های Location و X-Ride-Id بدهد."""
        c = TestClient(app)
        response = c.post(
            "/rides",
            json={"origin": "Tajrish", "destination": "Vanak", "price": 100000},
        )
        self.assertEqual(response.status_code, 201)
        new_id = response.json()["id"]
        self.assertEqual(response.headers["location"], f"/rides/{new_id}")
        self.assertEqual(response.headers["x-ride-id"], str(new_id))

    def test_session_endpoint_sets_device_id_cookie(self):
        """مسیر /session باید کوکی device_id را روی پاسخ بنشاند."""
        c = TestClient(app)
        response = c.get("/session")
        self.assertEqual(response.status_code, 200)
        self.assertIn("device_id", response.cookies)


if __name__ == "__main__":
    unittest.main()
