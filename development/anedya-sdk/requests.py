# anedya_sdk/requests.py
import requests

class AnedyaHTTP:
    def __init__(self, base_url):
        self.base_url = base_url

    def send_request(self, method, endpoint, data=None, headers=None):
        # Implement HTTP request functionality here
        url = self.base_url + endpoint
        response = requests.request(method, url, data=data, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}")
        return response.json()

    def get_data(self, device_id, start_time, end_time):
        # Implement an HTTP GET request to retrieve device data
        endpoint = f"/devices/{device_id}/data?start={start_time}&end={end_time}"
        return self.send_request("GET", endpoint)
