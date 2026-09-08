import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class SampleTests(unittest.TestCase):
    def test_products_default_page_size_is_ten(self):
        """بدون پارامتر، اندازهٔ پیش‌فرض صفحه باید ۱۰ باشد و ده قلم برگردد."""
        body = client.get("/products").json()
        self.assertEqual(body["size"], 10)
        self.assertEqual(len(body["items"]), 10)

    def test_products_second_page_returns_next_slice(self):
        """صفحهٔ دوم با size=5 باید بازهٔ بعدی محصولات را برگرداند."""
        body = client.get("/products", params={"page": 2, "size": 5}).json()
        self.assertEqual(body["page"], 2)
        self.assertEqual(len(body["items"]), 5)

    def test_orders_uses_the_same_pagination_dependency(self):
        """مسیر /orders باید با همان وابستگی صفحه‌بندی کار کند."""
        body = client.get("/orders", params={"size": 4}).json()
        self.assertEqual(body["size"], 4)
        self.assertEqual(len(body["items"]), 4)


if __name__ == "__main__":
    unittest.main()
