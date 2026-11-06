import requests
from configs.settings import BASE_URL, DEFAULT_USER_EMAIL, DEFAULT_USER_PASSWORD

class APIClient:
    def __init__(self, authenticated=True, email=DEFAULT_USER_EMAIL, password=DEFAULT_USER_PASSWORD):
        self.headers = {}
        self.authenticated = authenticated

        if authenticated:
            access_token = self.login(email, password)
            self.headers["Authorization"] = f"Bearer {access_token}"

    def login(self, email, password):
        url = f"{BASE_URL}/api/v1/auth/login"

        payload = {
            "email": email,
            "password": password
        }

        response_body = self.post_json(url, data=payload)

        return response_body["access_token"]

    def get(self, url, headers=None):
        headers = self.build_headers(headers)
        response = requests.get(url, headers=headers)

        assert response.status_code == 200, f"Status code expected 200, actual {response.status_code}"

        return response

    def get_json(self, url, headers=None):
        headers = self.build_headers(headers)
        response = self.get(url, headers)

        return response.json()

    def post(self, url, data, headers=None, expected_status_code=200):
        headers = self.build_headers(headers)
        response = requests.post(url, json=data, headers=headers)

        assert response.status_code == expected_status_code, f"Status code expected {expected_status_code}, actual {response.status_code}"

        return response

    def post_json(self, url, data, headers=None, expected_status_code=200):
        headers = self.build_headers(headers)
        response = self.post(url, data, headers, expected_status_code)

        return response.json()

    def build_headers(self, headers=None):
        if self.authenticated:
            return {**self.headers, **(headers or {})} # Combining two dictionaries
        return headers