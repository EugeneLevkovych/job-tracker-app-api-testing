from configs.settings import BASE_URL
from clients.api_client import APIClient

# The client will make the call and return the json body of the response 
api_client = APIClient()

def test_verify_user_can_login_with_valid_credentials():
    """	
    Example response body:
    {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJzdHVkZW50QGV4YW1wbGUuY29tIiwicm9sZSI6InVzZXIiLCJpYXQiOjE3OTM2MTYyODYsImV4cCI6MTc5MzY0NTA4Nn0.1TkU-RM7rnHclYPVoWA-98VvlBO9cTzwv8RX2BKYDiQ",
     "token_type": "bearer",
     "expires_in": 28800,
     "user": {
     "id": 1,
     "email": "student@example.com",
     "full_name": "SupersQA Student",
     "role": "user",
     "is_active": true,
     "created_at": "2026-08-06T00:01:52",
     "updated_at": "2026-08-06T00:01:52"
     }
    }
    """
    # make the call
    endpoint = "/api/v1/auth/login"
    
    payload = {
        "email": "student@example.com",
        "password": "Password123!"
        }
   
    
    response_body = api_client.post_json(endpoint, data=payload)
  
    assert response_body ["access_token"], f"Access token is required, but got {response_body}"
    assert response_body ["token_type"] == "bearer", "Token type is required"
    assert response_body ["expires_in"], f"Expires in is required but got {response_body['expires_in']}"
    assert response_body ["user"], f"User is required, but got {response_body['user']}"
    assert response_body ["user"]["id"], f"User ID is required, but got {response_body['user']['id']}"
    assert response_body ["user"]["email"] == payload["email"], f"User email is required, but got {response_body['user']['email']}"
    assert response_body ["user"]["full_name"], f"User full_name is required, but got {response_body['user']['full_name']}"
    assert response_body ["user"]["role"], f"User role is required, but got {response_body['user']['role']}"
    assert response_body ["user"]["is_active"], f"User is_active is required, but got {response_body['user']['is_active']}"
    assert response_body ["user"]["created_at"], f"User created_at is required, but got {response_body['user']['created_at']}"
    assert response_body ["user"]["updated_at"], f"User updated_at is required, but got {response_body['user']['updated_at']}"

def test_verify_user_can_not_login_with_invalid_credentials():
    """
    Example response body:
    {
      "error": {
      "code": "INVALID_CREDENTIALS",
      "message": "Invalid email or password",
      "details": []
     }
    }
    """

    # make the call
    endpoint = "/api/v1/auth/login"
    
    payload = {
        "email": "student@example.com",
        "password": "Password1234"
        }

    
    response_body = api_client.post_json(endpoint, data=payload, expected_status_code=401)
  

    # verify the response body

    assert isinstance(response_body["error"], dict), f"Expected 'error' to be a dict, but got {type(response_body['error']).__name__}: {response_body['error']}"
    error = response_body["error"]
    assert error["code"] == "INVALID_CREDENTIALS", f"Expected code 'INVALID_CREDENTIALS', but got {error['code']}"
    assert error["message"] == "Invalid email or password", f"Unexpected message: {error['message']}"
    assert isinstance(error["details"], list), f"Expected 'details' to be a list, but got {type(error['details']).__name__}"