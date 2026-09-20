import os
import sys
import time
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class SampleTests(unittest.TestCase):
    def test_health_endpoint_returns_status_code_200_on_root_path(self):
        """مسیر / باید با کد ۲۰۰ و یک شیء JSON پاسخ دهد."""
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)

    def test_aggregate_known_token_returns_full_shape(self):
        """تجمیع برای QP-1001 باید found=True و جزئیات آگهی را بدهد."""
        body = client.get("/aggregate/QP-1001").json()
        self.assertIs(body["found"], True)
        self.assertEqual(body["post"]["city"], "Tehran")
        self.assertEqual(body["seller"]["name"], "Kaveh")
        self.assertEqual(body["sources_count"], 5)

    def test_aggregate_unknown_token_returns_partial(self):
        """تجمیع برای آگهی ناموجود باید found=False و post برابر None بدهد."""
        body = client.get("/aggregate/QP-9999").json()
        self.assertIs(body["found"], False)
        self.assertIsNone(body["post"])
        self.assertEqual(body["similar"], [])

    def test_batch_endpoint_aggregates_two_tokens(self):
        """batch برای دو شناسه باید دو آیتم تجمیع‌شده بدهد."""
        body = client.get("/batch?tokens=QP-1001,QP-1002").json()
        self.assertEqual(body["requested"], 2)
        self.assertEqual(len(body["items"]), 2)

    def test_single_aggregate_call_runs_sources_concurrently(self):
        """یک فراخوانی تجمیع باید بسیار کمتر از مجموع تأخیر منابع طول بکشد."""
        start = time.perf_counter()
        client.get("/aggregate/QP-1002")
        elapsed = time.perf_counter() - start
        self.assertLess(elapsed, 0.6)


if __name__ == "__main__":
    unittest.main()
