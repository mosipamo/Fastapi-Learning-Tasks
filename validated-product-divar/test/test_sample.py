import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pydantic import ValidationError

from fastapi.testclient import TestClient

from main import app
from models import ProductIn

client = TestClient(app)


VALID = {
    "title": "Apple iPhone 13",
    "price": 32_000_000,
    "category": "electronics",
    "city": "Tehran",
    "description": "Like new, with box.",
    "seller_phone": "09120000000",
}


class SampleTests(unittest.TestCase):
    def test_product_in_accepts_a_fully_valid_payload_without_error(self):
        """مدل ProductIn باید دادهٔ معتبر را بپذیرد و عنوان را نگه دارد."""
        product = ProductIn(**VALID)
        self.assertEqual(product.title, "Apple iPhone 13")

    def test_category_validator_rejects_an_unknown_category_value(self):
        """دسته‌بندی خارج از فهرست مجاز باید رد شود."""
        bad = dict(VALID, category="food")
        with self.assertRaises(ValidationError):
            ProductIn(**bad)

    def test_create_product_returns_status_code_200_for_valid_body(self):
        """ثبت آگهی با بدنهٔ معتبر باید کد ۲۰۰ بدهد."""
        self.assertEqual(client.post("/products", json=VALID).status_code, 200)

    def test_create_product_response_does_not_expose_seller_phone(self):
        """پاسخ ثبت آگهی نباید فیلد seller_phone را افشا کند."""
        out = client.post("/products", json=VALID).json()
        self.assertNotIn("seller_phone", out)


if __name__ == "__main__":
    unittest.main()
