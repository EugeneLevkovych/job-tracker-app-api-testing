from clients.api_client import APIClient

def test_verify_user_can_create_application():

    # create a payload
    payload = {
        "company_name": "SuperSQA",
        "job_url": "https://supersqa.com/jobs/ui-test-engineer",
        "location": "Remote",
        "next_action": "Follow up with manager",
        "notes": "Submitted through api testing.",
        "remote_type": "remote",
        "role_title": "API Test Engineer",
        "salary_range": "$170k - $200k",
        "status": "applied"
    }

    # make the api call

    endpoint = "/api/v1/applications"

    api_client = APIClient()

    create_application_json = api_client.post_json(endpoint, payload, expected_status_code=201)

    # verify the response
    assert isinstance(create_application_json["id"], int), f"Create application endpoint response ID is not integer. Actual: {create_application_json["id"]}"
    for field, expected_value in payload.items():
        actual_value = create_application_json[field]
        assert actual_value == expected_value, f"Create application endpoint response field '{field}' is incorrect. Expected: {expected_value}, Actual: {actual_value}"
    assert create_application_json["description"] == None
    # do a get call and verify the item is actualy created
    application_id = create_application_json["id"]
    get_application_endpoint = f"/api/v1/applications/{application_id}"
    get_response = api_client.get_json(get_application_endpoint)

    assert create_application_json["id"] == get_response["id"]
    for field, expected_value in payload.items():
        actual_value = get_response[field]
        assert actual_value == expected_value, f"Create application endpoint response field '{field}' is incorrect. Expected: {expected_value}, Actual: {actual_value}"
    assert get_response["description"] == None
    

    # clean up / teardown - Delete the application we created
    delete_endpoint = f"/api/v1/applications/{application_id}"
    # we just make the call, the client verifies 204 response and that is good enough
    api_client.delete(delete_endpoint)