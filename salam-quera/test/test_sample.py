import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class SampleTests(unittest.TestCase):
    """چند تست نمونه برای محک‌زدن سریع پیاده‌سازی پیش از ارسال."""

    def test_root_endpoint_returns_app_quera_hello(self):
        """مسیر / باید پاسخ ۲۰۰ بدهد و کلید app آن برابر quera-hello باشد."""
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("app"), "quera-hello")

    def test_health_endpoint_returns_status_ok(self):
        """مسیر /health باید پاسخ {\"status\": \"ok\"} بدهد."""
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_ping_endpoint_returns_pong(self):
        """مسیر /ping باید پاسخ {\"ping\": \"pong\"} بدهد."""
        response = client.get("/ping")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"ping": "pong"})

    def test_info_endpoint_returns_service_quera_hello(self):
        """مسیر /info باید پاسخ ۲۰۰ بدهد و کلید service آن برابر quera-hello باشد."""
        response = client.get("/info")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("service"), "quera-hello")

    def test_services_endpoint_returns_a_list(self):
        """مسیر /services باید پاسخ ۲۰۰ بدهد و بدنهٔ آن یک فهرست باشد."""
        response = client.get("/services")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_stats_endpoint_reports_three_members(self):
        """مسیر /stats باید پاسخ ۲۰۰ بدهد و کلید members آن برابر ۳ باشد."""
        response = client.get("/stats")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("members"), 3)

    def test_responses_welcome_payload_returns_dict(self):
        """تابع welcome_payload در فایل responses باید یک دیکشنری با کلید app برگرداند."""
        from responses import welcome_payload

        payload = welcome_payload()
        self.assertIsInstance(payload, dict)
        self.assertEqual(payload.get("app"), "quera-hello")


if __name__ == "__main__":
    unittest.main()
