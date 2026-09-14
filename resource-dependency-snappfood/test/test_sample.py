import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient

import menu_resource
from main import API_KEY, app

# نگهبان سراسری روی همهٔ مسیرها اعمال می‌شود، پس کلاینت نمونه باید سربرگ کلید را
# بفرستد. کلاینت بدون کلید برای آزمودن خود نگهبان جداگانه ساخته شده است.
client = TestClient(app, headers={"X-Api-Key": API_KEY})
client_no_key = TestClient(app)


class SampleTests(unittest.TestCase):
    def test_menu_item_returns_record_for_known_item(self):
        """مسیر /menu/1 باید رکورد آیتم یک را برگرداند."""
        body = client.get("/menu/1").json()
        self.assertEqual(body["id"], 1)
        self.assertEqual(body["name"], "Pizza Margherita")

    def test_teardown_runs_after_successful_request(self):
        """پس از یک درخواست موفق، اتصال باید بسته شود (close ثبت شود)."""
        menu_resource.reset_events()
        client.get("/menu/2")
        closes = [e for e in menu_resource.EVENTS if e[0] == "close"]
        self.assertEqual(len(closes), 1)

    def test_teardown_runs_after_404(self):
        """پس از خطای ۴۰۴ هم اتصال باید بسته شود."""
        menu_resource.reset_events()
        self.assertEqual(client.get("/menu/999").status_code, 404)
        closes = [e for e in menu_resource.EVENTS if e[0] == "close"]
        self.assertEqual(len(closes), 1)

    def test_request_without_api_key_is_rejected_with_401(self):
        """درخواست بدون سربرگ X-Api-Key باید با کد ۴۰۱ رد شود."""
        self.assertEqual(client_no_key.get("/menu/1").status_code, 401)

    def test_guard_applies_to_root_path_too(self):
        """نگهبان باید روی مسیر / هم اعمال شود، نه فقط روی مسیرهای منو."""
        self.assertEqual(client_no_key.get("/").status_code, 401)
        self.assertEqual(client.get("/").status_code, 200)

    def test_menu_listing_returns_pagination_keys(self):
        """مسیر /menu باید کلیدهای page و size و total و items را برگرداند."""
        body = client.get("/menu", params={"page": 1, "size": 3}).json()
        self.assertEqual(body["page"], 1)
        self.assertEqual(body["size"], 3)
        self.assertEqual(body["total"], 5)
        self.assertEqual(len(body["items"]), 3)


if __name__ == "__main__":
    unittest.main()
