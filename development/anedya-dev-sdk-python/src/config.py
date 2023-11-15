# src/config.py

from datetime import datetime
import paho.mqtt.client as mqtt
import ssl
import time

class AnedyaSDK:
    def __init__(self, device_id, api_token, connection_mode, timeout=60, max_buffer_size=10, tls_certificate=None):
        self.device_id = device_id
        self.api_token = api_token
        self.connection_mode = connection_mode
        self.timeout = timeout
        self.max_buffer_size = max_buffer_size
        self.tls_certificate = tls_certificate
        self.time_format = "%Y-%m-%d %H:%M:%S"
        self.buffer = []

    def send_data(self, data):
        timestamp = time.strftime(self.time_format)
        formatted_data = f"{timestamp} - {data}"
        self.buffer.append(formatted_data)

    def push_data(self):
        if len(self.buffer) >= self.max_buffer_size or self.max_buffer_size == 0:
            self._push_data_to_cloud()
            self.buffer.clear()

    def set_timeout(self, new_timeout):
        self.timeout = new_timeout

    def set_max_buffer_size(self, new_max_buffer_size):
        self.max_buffer_size = new_max_buffer_size

    def set_connection_mode(self, new_connection_mode):
        self.connection_mode = new_connection_mode

    def set_tls_certificate(self, new_tls_certificate):
        self.tls_certificate = new_tls_certificate

    def _push_data_to_cloud(self):
        client = self._connect_mqtt()
        # Implement logic to push data to the cloud based on the connection mode
        print(f"Pushing data to the cloud: {self.buffer}")
        client.disconnect()

    def _connect_mqtt(self):
        client = mqtt.Client()
        if self.tls_certificate:
            client.tls_set(certfile=self.tls_certificate, tls_version=ssl.PROTOCOL_TLS)
        # Connect to the MQTT broker
        client.connect("mqtt.eclipse.org", 1883, 60)
        return client

