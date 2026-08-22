import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class SampleTests(unittest.TestCase):
    def test_welcome_endpoint_returns_status_code_200_on_root_path(self):
        """The / path should respond with status 200 and a JSON object."""
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)

    def test_products_endpoint_applies_default_page_and_page_size_values(self):
        """Without parameters, page=1, page_size=10, and the first ten items should be returned."""
        body = client.get("/products").json()
        self.assertEqual(body["page"], 1)
        self.assertEqual(body["page_size"], 10)
        self.assertEqual(body["total"], 22)
        self.assertEqual([i["id"] for i in body["items"]], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_products_endpoint_filters_by_case_insensitive_name_substring(self):
        """With q=milk, the two milk products should be returned."""
        body = client.get("/products", params={"q": "milk"}).json()
        self.assertEqual(body["total"], 2)
        self.assertEqual([i["id"] for i in body["items"]], [1, 2])

    def test_products_endpoint_filters_by_exact_category_match(self):
        """With category=fruit, the five fruits should be returned."""
        body = client.get("/products", params={"category": "fruit"}).json()
        self.assertEqual(body["total"], 5)


if __name__ == "__main__":
    unittest.main()
