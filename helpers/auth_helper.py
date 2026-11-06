from configs.settings import BASE_URL, DEFAULT_USER_EMAIL, DEFAULT_USER_PASSWORD
from clients.api_client import APIClient

def login_user(email=DEFAULT_USER_EMAIL, password=DEFAULT_USER_PASSWORD):
    # get JWT token
    # login with user and get the token from the response
    # make the call
    url = f"{BASE_URL}/api/v1/auth/login"
    
    payload = {
        "email": email,
        "password": password
        }
    
    api_client = APIClient()
    response_body = api_client.post_json(url, data=payload)    
    
    return response_body["access_token"]