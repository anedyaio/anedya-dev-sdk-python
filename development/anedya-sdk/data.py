# anedya_sdk/data.py
from datetime import datetime

class DataProcessor:
    def __init__(self, data):
        self.data = data

    def process_data(self):
        # Implement data processing and formatting logic, including time format
        processed_data = self.data

        # Convert timestamps to datetime objects using the default time format
        for entry in processed_data:
            entry['timestamp'] = datetime.strptime(entry['timestamp'], '%Y-%m-%d %H:%M:%S')

        return processed_data
