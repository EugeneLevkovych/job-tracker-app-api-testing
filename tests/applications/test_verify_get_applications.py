from configs.settings import BASE_URL
import requests

def test_verify_authenticated_user_can_get_applications():

    # get JWT token
    # login with user and get the token from the response
    # make the call
    url = f"{BASE_URL}/api/v1/auth/login"
    
    payload = {
        "email": "student@example.com",
        "password": "Password123!"
        }
    response = requests.post(url, json=payload)

    assert response.status_code == 200, f"Expected status code is 200, but got {response.status_code}"
   
    response_body = response.json()
    access_token = response_body ["access_token"]

    # make the api call with the token in the header
    get_applications_url = f"{BASE_URL}/api/v1/applications"

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(get_applications_url, headers=headers)
   

    # verify the api status code
    assert response.status_code == 200, f"Get applications api response expected to be 200 actual was  {response.status_code}. Endpoint: '/api/v1/applications'."

    # verify the api response body
    response_body = response.json()
    assert response_body, "Expected some data in response body but it was empty or None."
    assert isinstance(response_body, list), f"Expected the response body to be a list but got {type(response_body)}."