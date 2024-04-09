from enum import Enum
import uuid


class ConnectionMode(Enum):
    HTTP = "HTTP"
    MQTT = "MQTT"


class MQTTMode(Enum):
    TCP = "TCP"
    WSS = "WSS"


class Encoding(Enum):
    JSON = "JSON"
    CBOR = "CBOR"


class AnedyaConfig:
    def __init__(self):
        """
        Anedya SDK Configuration.

        Args:
            device_id (str): The device's unique identifier.
            api_token (str): The API token for cloud service access.
            connection_mode (ConnectionMode): The mode for data transmission (HTTP or MQTT).
            timeout (int): Timeout duration (0 for instant push).
            max_buffer_size (int): The maximum data buffer size (default
            or user-defined).
            tls_certificate (Optional[str]): Path to the TLS certificate file 
            if using MQTT. Defaults to None.
        """

        self.connection_mode = ConnectionMode.MQTT
        self.mqtt_mode = MQTTMode.TCP
        self.timeout = 60
        self.max_buffer_size = 10
        self.connection_key = None
        self.region = "ap-in-1"
        self.connection_key = ""
        self.authmode = 'key'
        self.on_connect = None
        self.on_disconnect = None
        self.on_message = None

        # Internal Variables - Do not modify them directly
        self._deviceID = None
        self._deviceid_set = False
        self._security_set = False
        self._testmode = False

    def set_connection_key(self, key):
        """
        Set a connection key
        """
        self.connection_key = key

    def set_deviceid(self, id: str):
        """
        Set DeviceID
        """
        self._deviceID = uuid.UUID(id)
        self._deviceid_set = True

    def set_timeout(self, timeout):
        """
        Set timeout for automatic flush of the data
        """
        self.timeout = timeout

    def set_maxbuffer_size(self, buffersize):
        """
        Set maximum buffer size
        """
        self.max_buffer_size = buffersize

    def set_region(self, region):
        """
        Set region
        """
        self.region = region

    def set_on_connect(self, callback):
        """
        Set on connect callback
        """
        self.on_connect = callback

    def set_on_disconnect(self, callback):
        """
        Set on disconnect callback
        """
        self.on_disconnect = callback

    def set_on_message(self, callback):
        """
        Set on message callback
        """
        self.on_message = callback


def default_config():
    defconfig = AnedyaConfig()
    return defconfig
