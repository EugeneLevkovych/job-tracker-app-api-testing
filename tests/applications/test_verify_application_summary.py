from clients.api_client import APIClient
from helpers.auth_helper import login_user

def test_verify_authenticated_user_can_get_applications_summary():
    """
    Example response body:
    {
    "potential": 2,
    "applied": 1,
    "in_progress": 1,
    "final_stage": 0,
    "hired": 0,
    "rejected": 0,
    "withdrawn": 0,
    "total": 4
    }
    """

  

    # make the call with the token in the header
    applications_summary_endpoint = "/api/v1/applications/summary"

    api_client = APIClient()

    response_body = api_client.get_json(applications_summary_endpoint)

    # verify the response body
   
    assert response_body, "Expected response but got empty or null. Endpoint: /api/v1/applications/summary"

    assert isinstance(response_body["potential"], int), f"Expected integer in the response body 'potential' field but got {response_body["potential"]}"
    assert isinstance(response_body["applied"], int), f"Expected integer in the response body 'applied' field but got {response_body["applied"]}"
    assert isinstance(response_body["in_progress"], int), f"Expected integer in the response body 'in_progress' field but got {response_body["in_progress"]}"
    assert isinstance(response_body["final_stage"], int), f"Expected integer in the response body 'final_stage' field but got {response_body["final_stage"]}"
    assert isinstance(response_body["hired"], int), f"Expected integer in the response body 'hired' field but got {response_body["hired"]}"
    assert isinstance(response_body["rejected"], int), f"Expected integer in the response body 'rejected' field but got {response_body["rejected"]}"
    assert isinstance(response_body["withdrawn"], int), f"Expected integer in the response body 'withdrawn' field but got {response_body["withdrawn"]}"
    assert isinstance(response_body["total"], int), f"Expected integer in the response body 'total' field but got {response_body["total"]}"