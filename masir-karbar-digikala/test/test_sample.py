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

    def test_user_endpoint_returns_exact_record_for_user_one(self):
        """The /users/1 path should return the full record of user one."""
        body = client.get("/users/1").json()
        self.assertEqual(body, {"id": 1, "name": "Ali Rezvani", "city": "Tehran", "is_plus": True})

    def test_order_endpoint_returns_exact_record_for_order_one_zero_one(self):
        """The two-level path /users/1/orders/101 should return the record of order 101."""
        body = client.get("/users/1/orders/101").json()
        self.assertEqual(body["id"], 101)
        self.assertEqual(body["title"], "Wireless Mouse")

    def test_user_orders_endpoint_returns_two_orders_for_user_one(self):
        """The /users/1/orders path should return the two orders of user one."""
        body = client.get("/users/1/orders").json()
        self.assertIsInstance(body, list)
        self.assertEqual(len(body), 2)

    def test_user_summary_endpoint_reports_total_amount_for_user_one(self):
        """The /users/1/summary path should report a total amount of 3250000."""
        body = client.get("/users/1/summary").json()
        self.assertEqual(body.get("total_amount"), 3250000)

    def test_user_endpoint_returns_422_when_user_id_is_not_an_integer(self):
        """A non-numeric value in the user path should return status 422."""
        self.assertEqual(client.get("/users/abc").status_code, 422)


if __name__ == "__main__":
    unittest.main()
