# anedya_sdk/examples/usage_example.py
from anedya_sdk import AnedyaSDK

user_id = "your_user_id"
password = "your_password"
api_key = "your_api_key"
base_url = "https://api.anedya.com"

sdk = AnedyaSDK(user_id, password, api_key, base_url)
device_id = "your_device_id"
start_time = "2023-01-01T00:00:00"
end_time = "2023-02-01T00:00:00"

data = sdk.get_data(device_id, start_time, end_time)
sdk.visualize_data(data)
