# anedya_sdk/client.py
import requests
from .requests import AnedyaHTTP
from .data import DataProcessor
from .visualization import Visualization

class AnedyaSDK:
    def __init__(self, user_id, password, api_key, base_url):
        self.user_id = user_id
        self.password = password
        self.api_key = api_key
        self.base_url = base_url
        self.http = AnedyaHTTP(self.base_url)

    def get_data(self, device_id, start_time, end_time):
        # Implement functionality to fetch data using HTTP
        response = self.http.get_data(device_id, start_time, end_time)
        processed_data = DataProcessor(response).process_data()
        return processed_data

    def visualize_data(self, data):
        # Implement data visualization functionality using the Visualization module
        return Visualization.plot(data)
