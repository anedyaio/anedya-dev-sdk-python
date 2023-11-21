from datetime import datetime
import paho.mqtt.client as mqtt
import ssl
import time
from enum import Enum
from typing import Optional

class ConnectionMode(Enum):
    HTTP = "HTTP"
    MQTT = "MQTT"

class AnedyaConfig:
    def __init__(self, device_id: str, api_token: str, connection_mode: ConnectionMode = ConnectionMode.HTTP, timeout: int = 60, max_buffer_size: int = 10, tls_certificate: Optional[str] = None):
        """
        Anedya SDK Configuration.

        Args:
            device_id (str): The device's unique identifier.
            api_token (str): The API token for cloud service access.
            connection_mode (ConnectionMode): The mode for data transmission (HTTP or MQTT).
            timeout (int): Timeout duration (0 for instant push).
            max_buffer_size (int): The maximum data buffer size (default or user-defined).
            tls_certificate (Optional[str]): Path to the TLS certificate file if using MQTT. Defaults to None.
        """
        self.device_id = device_id
        self.api_token = api_token
        self.connection_mode = connection_mode
        self.timeout = timeout
        self.max_buffer_size = max_buffer_size
        self.tls_certificate = tls_certificate

class AnedyaSDK:
    def __init__(self, config: AnedyaConfig):
        """
        Initialize the Anedya SDK.

        Args:
            config (AnedyaConfig): Anedya SDK configuration.
        """
        self.config = config
        self.time_format = "%Y-%m-%d %H:%M:%S"
        self.buffer = []

    def send_data(self, data: str):
        """
        Add data to the buffer with timestamp.

        Args:
            data (str): Data to be sent to the cloud.
        """
        timestamp = time.strftime(self.time_format)
        formatted_data = f"{timestamp} - {data}"
        self.buffer.append(formatted_data)

    def push_data(self):
        """
        Push data to the cloud if buffer conditions are met.
        """
        if len(self.buffer) >= self.config.max_buffer_size or self.config.max_buffer_size == 0:
            self._push_data_to_cloud()
            self.buffer.clear()

    def set_timeout(self, new_timeout: int):
        """
        Set the timeout duration.

        Args:
            new_timeout (int): New timeout duration.
        """
        self.config.timeout = new_timeout

    def set_max_buffer_size(self, new_max_buffer_size: int):
        """
        Set the maximum buffer size.

        Args:
            new_max_buffer_size (int): New maximum buffer size.
        """
        self.config.max_buffer_size = new_max_buffer_size

    def set_connection_mode(self, new_connection_mode: ConnectionMode):
        """
        Set the connection mode.

        Args:
            new_connection_mode (ConnectionMode): New connection mode.
        """
        self.config.connection_mode = new_connection_mode

    def set_tls_certificate(self, new_tls_certificate: Optional[str]):
        """
        Set the TLS certificate path.

        Args:
            new_tls_certificate (Optional[str]): Path to the TLS certificate file if using MQTT.
        """
        self.config.tls_certificate = new_tls_certificate

    def _push_data_to_cloud(self):
        """
        Push data to the cloud using the configured connection mode.
        """
        client = self._connect_mqtt()
        # Implement logic to push data to the cloud based on the connection mode
        print(f"Pushing data to the cloud: {self.buffer}")
        client.disconnect()

    def _connect_mqtt(self) -> mqtt.Client:
        """
        Connect to the MQTT broker.

        Returns:
            mqtt.Client: MQTT client instance.
        """
        client = mqtt.Client()
        if self.config.tls_certificate:
            client.tls_set(certfile=self.config.tls_certificate, tls_version=ssl.PROTOCOL_TLS)
        # Connect to the MQTT broker
        client.connect("mqtt.eclipse.org", 1883, 60)
        return client
