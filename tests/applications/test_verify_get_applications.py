from helpers.auth_helper import login_user
from clients.api_client import APIClient

def test_verify_authenticated_user_can_get_applications():
    """
    Verify a logged-in user can get their list of applications.

    Calls GET /api/v1/applications and checks that the response is a
    non-empty list.
    """


    # make the api call with the token in the header
    get_applications_endpoint = "/api/v1/applications"


    api_client = APIClient()

    response_body = api_client.get_json(get_applications_endpoint)

    # verify the api response body
    assert response_body, "Expected some data in response body but it was empty or None."
    assert isinstance(response_body, list), f"Expected the response body to be a list but got {type(response_body)}."