# test_config.py
from config import AnedyaSDK

def test_sdk_functionality():
    config = AnedyaConfig(device_id="device_id", api_token="api_token", connection_mode="MQTT", timeout=60,
                          max_buffer_size=10, tls_certificate="tls_certificate.pem")
    sdk = AnedyaSDK(config)

    sdk.send_data("Sensor Data 1")
    sdk.send_data("Sensor Data 2")

    sdk.push_data()

    sdk.set_timeout(120)
    sdk.set_max_buffer_size(20)

    sdk.send_data("Sensor Data 3")
    sdk.push_data()

    sdk.set_connection_mode("HTTP")
    # Implement logic for retrieving data if needed
    print("Retrieving data from the cloud")

if __name__ == "__main__":
    test_sdk_functionality()
