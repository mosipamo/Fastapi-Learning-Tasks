import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class SampleTests(unittest.TestCase):
    def test_welcome_endpoint_returns_status_code_200_on_root_path(self):
        """مسیر / باید با کد ۲۰۰ و یک شیء JSON پاسخ دهد."""
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)

    def test_signup_endpoint_returns_status_code_200_for_valid_body(self):
        """ثبت‌نام با بدنهٔ کامل و معتبر باید کد ۲۰۰ بدهد."""
        body = {"username": "sample", "email": "sample@example.com", "password": "pwpwpwpw", "age": 22}
        response = client.post("/signup", json=body)
        self.assertEqual(response.status_code, 200)

    def test_signup_response_does_not_contain_raw_password_field(self):
        """رمز عبور خام نباید در پاسخ ثبت‌نام باشد."""
        body = {"username": "sample2", "email": "s2@example.com", "password": "topsecret"}
        out = client.post("/signup", json=body).json()
        self.assertNotIn("password", out)

    def test_signup_endpoint_returns_422_when_username_is_missing(self):
        """نبودِ فیلد اجباری username باید کد ۴۲۲ بدهد."""
        body = {"email": "x@example.com", "password": "pwpwpwpw"}
        self.assertEqual(client.post("/signup", json=body).status_code, 422)

    def test_account_detail_returns_found_true_for_existing_username(self):
        """خواندن یک حساب موجود با مسیر /accounts/{username} باید found=true بدهد."""
        client.post("/signup", json={"username": "s_detail", "email": "d@e.com", "password": "pwpwpwpw"})
        out = client.get("/accounts/s_detail").json()
        self.assertIs(out.get("found"), True)

    def test_login_returns_authenticated_true_for_correct_password(self):
        """ورود با رمز درست باید authenticated=true بدهد."""
        client.post("/signup", json={"username": "s_login", "email": "l@e.com", "password": "rightpass"})
        out = client.post("/login", json={"username": "s_login", "password": "rightpass"}).json()
        self.assertIs(out.get("authenticated"), True)


if __name__ == "__main__":
    unittest.main()
