import requests

class APIClient:
    def __init__(self):
        pass

    def get(self, url, headers):
        response = requests.get(url, headers=headers)

        assert response.status_code == 200, f"Status code expectet 200, actual {response.status_code}"

        return response

    def get_json(self, url, headers):
        response = self.get(url, headers)

        return response.json()