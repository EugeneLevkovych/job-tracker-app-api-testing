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
        endpoint = "/api/v1/auth/login"

        payload = {
            "email": email,
            "password": password
        }

        response_body = self.post_json(endpoint, data=payload)

        return response_body["access_token"]

    def get(self, endpoint, headers=None, expected_status_code=200):
        headers = self.build_headers(headers)
        url = self.build_url(endpoint)
        response = requests.get(url, headers=headers)

        self.verify_status_code(response, expected_status_code, url)

        return response

    def get_json(self, endpoint, headers=None, expected_status_code=200):
        response = self.get(endpoint, headers, expected_status_code)

        return response.json()

    def post(self, endpoint, data, headers=None, expected_status_code=200):
        headers = self.build_headers(headers)
        url = self.build_url(endpoint)
        response = requests.post(url, json=data, headers=headers)
        self.verify_status_code(response, expected_status_code, url)
        return response

    def post_json(self, endpoint, data, headers=None, expected_status_code=200):
        response = self.post(endpoint, data, headers, expected_status_code)

        return response.json()

    def build_headers(self, headers=None):
        if self.authenticated:
            return {**self.headers, **(headers or {})} # Combining two dictionaries
        return headers

    def verify_status_code(self, response, expected_status_code, url):
        assert response.status_code == expected_status_code, f"Status code. Expected: {expected_status_code}, Actual: {response.status_code}, URL: {url}"

    def build_url(self, endpoint):
        return f"{BASE_URL}{endpoint}"   