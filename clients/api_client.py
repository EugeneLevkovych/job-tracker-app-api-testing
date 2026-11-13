"""
HTTP client for the Job Tracker API.

Wraps ``requests`` with base URL handling, optional bearer-token
authentication, status code verification and request/response logging.
"""

import logging

import requests
from configs.settings import BASE_URL, DEFAULT_USER_EMAIL, DEFAULT_USER_PASSWORD

logger = logging.getLogger(__name__)

SENSITIVE_FIELDS = {"password", "access_token"}
MAX_LOGGED_BODY_LENGTH = 500


class APIClient:
    """
    Client for sending requests to the Job Tracker API in tests.

    When authenticated, the client logs in on creation and adds the
    access token to every request. Each request verifies the response
    status code and fails the test if it does not match.

    Example:
        >>> client = APIClient()
        >>> applications = client.get_json("/api/v1/applications")

    Attributes:
        headers (dict): Default headers sent with every request.
        authenticated (bool): Whether the client sends the auth header.
    """

    def __init__(self, authenticated=True, email=DEFAULT_USER_EMAIL, password=DEFAULT_USER_PASSWORD):
        """
        Creates the client and logs in if authentication is enabled.

        Args:
            authenticated (bool): If True, log in and send the access token
                with every request. Defaults to True.
            email (str): Email used to log in. Defaults to the configured user.
            password (str): Password used to log in. Defaults to the
                configured user.
        """
        self.headers = {}
        self.authenticated = authenticated

        if authenticated:
            access_token = self.login(email, password)
            self.headers["Authorization"] = f"Bearer {access_token}"
        else:
            logger.debug("APIClient created without authentication")

    def login(self, email, password):
        """
        Logs in a user and returns their access token.

        Args:
            email (str): User email.
            password (str): User password.

        Returns:
            str: JWT access token.

        Raises:
            AssertionError: If the login request does not return 200.
        """
        endpoint = "/api/v1/auth/login"

        payload = {
            "email": email,
            "password": password
        }

        logger.info("Logging in as %s", email)
        response_body = self.post_json(endpoint, data=payload)
        logger.info("Login successful for %s", email)

        return response_body["access_token"]

    def get(self, endpoint, headers=None, expected_status_code=200):
        """
        Sends a GET request and verifies the status code.

        Args:
            endpoint (str): API path, e.g. ``"/api/v1/applications"``.
            headers (dict, optional): Extra headers merged over the defaults.
            expected_status_code (int): Expected status code. Defaults to 200.

        Returns:
            requests.Response: The raw response.

        Raises:
            AssertionError: If the status code does not match.
        """
        headers = self.build_headers(headers)
        url = self.build_url(endpoint)

        logger.info("GET %s", url)
        response = requests.get(url, headers=headers)
        self.log_response(response)

        self.verify_status_code(response, expected_status_code, url)

        return response

    def get_json(self, endpoint, headers=None, expected_status_code=200):
        """
        Sends a GET request and returns the parsed JSON body.

        Args:
            endpoint (str): API path, e.g. ``"/api/v1/applications"``.
            headers (dict, optional): Extra headers merged over the defaults.
            expected_status_code (int): Expected status code. Defaults to 200.

        Returns:
            dict | list: Parsed response body.

        Raises:
            AssertionError: If the status code does not match.
        """
        response = self.get(endpoint, headers, expected_status_code)

        return response.json()

    def post(self, endpoint, data, headers=None, expected_status_code=200):
        """
        Sends a POST request with a JSON body and verifies the status code.

        Args:
            endpoint (str): API path, e.g. ``"/api/v1/auth/login"``.
            data (dict): Request body, sent as JSON.
            headers (dict, optional): Extra headers merged over the defaults.
            expected_status_code (int): Expected status code. Defaults to 200.

        Returns:
            requests.Response: The raw response.

        Raises:
            AssertionError: If the status code does not match.
        """
        headers = self.build_headers(headers)
        url = self.build_url(endpoint)

        logger.info("POST %s", url)
        logger.debug("Request body: %s", self.mask_sensitive(data))
        response = requests.post(url, json=data, headers=headers)
        self.log_response(response)

        self.verify_status_code(response, expected_status_code, url)
        return response

    def post_json(self, endpoint, data, headers=None, expected_status_code=200):
        """
        Sends a POST request and returns the parsed JSON body.

        Args:
            endpoint (str): API path, e.g. ``"/api/v1/auth/login"``.
            data (dict): Request body, sent as JSON.
            headers (dict, optional): Extra headers merged over the defaults.
            expected_status_code (int): Expected status code. Defaults to 200.

        Returns:
            dict | list: Parsed response body.

        Raises:
            AssertionError: If the status code does not match.
        """
        response = self.post(endpoint, data, headers, expected_status_code)

        return response.json()

    def delete(self, endpoint, expected_status_code=204):
        headers = self.build_headers()
        url = self.build_url(endpoint)
        response = requests.delete(url, headers=headers)
        return response
    

    def build_headers(self, headers=None):
        """
        Combines the client's default headers with per-request headers.

        Per-request headers override the defaults. Unauthenticated clients
        send only the per-request headers.

        Args:
            headers (dict, optional): Headers for this request.

        Returns:
            dict | None: Headers to send.
        """
        if self.authenticated:
            return {**self.headers, **(headers or {})} # Combining two dictionaries
        return headers

    def verify_status_code(self, response, expected_status_code, url):
        """
        Asserts the response has the expected status code.

        Logs the response body as an error before failing.

        Args:
            response (requests.Response): Response to check.
            expected_status_code (int): Expected status code.
            url (str): Request URL, included in the failure message.

        Raises:
            AssertionError: If the status code does not match.
        """
        if response.status_code != expected_status_code:
            logger.error(
                "Unexpected status code for %s. Expected: %s, Actual: %s, Body: %s",
                url, expected_status_code, response.status_code, self.truncate(response.text),
            )
        assert response.status_code == expected_status_code, f"Status code. Expected: {expected_status_code}, Actual: {response.status_code}, URL: {url}"

    def build_url(self, endpoint):
        """
        Builds a full URL from the configured base URL and an endpoint.

        Args:
            endpoint (str): API path starting with ``/``.

        Returns:
            str: Full request URL.
        """
        return f"{BASE_URL}{endpoint}"

    def log_response(self, response):
        """
        Logs the status code and timing, and the body at DEBUG level.

        Args:
            response (requests.Response): Response to log.
        """
        logger.info(
            "Response: %s (%.0f ms)",
            response.status_code, response.elapsed.total_seconds() * 1000,
        )
        if logger.isEnabledFor(logging.DEBUG):
            try:
                body = self.mask_sensitive(response.json())
            except ValueError:
                body = response.text
            logger.debug("Response body: %s", self.truncate(str(body)))

    @staticmethod
    def mask_sensitive(data):
        """
        Hides sensitive fields such as passwords and tokens for logging.

        Only top-level keys of a dict are masked. Other values are
        returned unchanged.

        Args:
            data (Any): Request or response body.

        Returns:
            Any: A copy with sensitive values replaced by ``"***"``.
        """
        if isinstance(data, dict):
            return {key: "***" if key in SENSITIVE_FIELDS else value for key, value in data.items()}
        return data

    @staticmethod
    def truncate(text):
        """
        Shortens long text so logs stay readable.

        Args:
            text (str): Text to shorten.

        Returns:
            str: The text, cut to ``MAX_LOGGED_BODY_LENGTH`` characters if longer.
        """
        if len(text) > MAX_LOGGED_BODY_LENGTH:
            return f"{text[:MAX_LOGGED_BODY_LENGTH]}... [truncated]"
        return text
