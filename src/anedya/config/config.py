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
    def __init__(self):
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
        
        self._deviceid_set = False
        self._security_set = False
        self.connection_mode = ConnectionMode.HTTP
        self.timeout = 60
        self.max_buffer_size = 10
        self.connection_key = None
        self.region = "ap-in-1"

    def set_connection_key(self, key):
        """
        Set a connection key
        """
        self.connection_key = key

    def set_timeout(self, timeout):
        """
        Set timeout for automatic flush of the data
        """
        self.timeout = timeout

    def set_max_buffer_size(self, buffersize):
        """
        Set maximum buffer size
        """
        self.max_buffer_size = buffersize
    