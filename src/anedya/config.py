from enum import Enum
import uuid
from .errors import AnedyaInvalidConfig
from .models import CommandDetails, VSUpdate
from typing import Callable


class ConnectionMode(Enum):
    HTTP = "HTTP"
    MQTT = "MQTT"


class MQTTMode(Enum):
    TCP = "TCP"
    WSS = "WSS"


class Encoding(Enum):
    JSON = "JSON"
    CBOR = "CBOR"


class RegionCode(Enum):
    AP_IN_1 = "ap-in-1"


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
        self.on_command = None
        self.on_vsupdate = None

        # Internal Variables - Do not modify them directly
        self._deviceID = None
        self._deviceid_set = False
        self._security_set = False
        self._testmode = False

    def set_connection_key(self, key: str):
        """
        This method sets the connection key for the client

        Args:
            key (str): Connection key for the client
        """
        self.connection_key = key

    def set_deviceid(self, id: str):
        """
        This method sets the device ID for the client

        Args:
            id (str): A Unique physical device ID which should not change for the entire lifetime of the device. Requires a valid UUID

        Raises:
            AnedyaInvalidConfig: The provided device ID should be a valid UUID, otherwise this exception will be raised
        """
        try:
            self._deviceID = uuid.UUID(id)
        except ValueError:
            raise AnedyaInvalidConfig("Device ID needs to be valid UUID")
        self._deviceid_set = True

    def set_region(self, region: RegionCode):
        """
        This method sets the region for the client

        Args:
            region (RegionCode): Set the regioncode where your Anedya project is created.
        """
        self.region = region

    def set_on_connect(self, callback):
        """
        Set a callback function that will be called when the connection is established.

        Args:
            callback (function): A callback function that will be called when the connection is established. The callback function should not block.

        Raises:
            AnedyaInvalidConfig: Raised when the callback is not a valid function
        """
        if not callable(callback):
            raise AnedyaInvalidConfig(
                "Callback function needs to be a valid function")
        self.on_connect = callback

    def set_on_disconnect(self, callback):
        """
        Set a callback function that will be called when the connection is disconnected.

        Args:
            callback (function): A callback function that will be called when the connection is disconnected. The callback function should not block

        Raises:
            AnedyaInvalidConfig: Raised when the callback is not a valid function
        """
        if not callable(callback):
            raise AnedyaInvalidConfig(
                "Callback function needs to be a valid function")
        self.on_disconnect = callback

    def set_on_command(self, callback: Callable[[CommandDetails], None]):
        """
        Set a callback function that will be called when a command is received.

        Args:
            callback (function): A callback function that will be called when a command is received. The callback function should not block.

        Raises:
            AnedyaInvalidConfig: Raised when the callback is not a valid function
        """
        if not callable(callback):
            raise AnedyaInvalidConfig(
                "Callback function needs to be a valid function")
        self.on_command = callback

    def set_on_vsupdate(self, callback: Callable[[VSUpdate], None]):
        """
        Set a callback function that will be called when a valuestore update is updated.

        Args:
            callback (function): A callback function that will be called when a valuestore update is received. The callback function should not block.

        Raises:
            AnedyaInvalidConfig: Raised when the callback is not a valid function
        """
        if not callable(callback):
            raise AnedyaInvalidConfig(
                "Callback function needs to be a valid function")
        self.on_vsupdate = callback


def default_config():
    defconfig = AnedyaConfig()
    return defconfig
