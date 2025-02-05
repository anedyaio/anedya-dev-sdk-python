"""
    Copyright 2024 Anedya Systems Private Limited

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from .config import AnedyaConfig
from .errors import AnedyaInvalidConfig
from .config import ConnectionMode
from .config import MQTTMode
from .transaction import Transactions
from .client.certs import ANEDYA_CA_CERTS
from ssl import SSLContext
import requests
from paho.mqtt import client as mqtt
from paho.mqtt.client import MQTTv5
import ssl


class AnedyaClient:

    def __init__(self, config: AnedyaConfig):
        self.set_config(config)

        # Internal Parameters
        if config.connection_mode == ConnectionMode.MQTT:
            # MQTT Related setup
            self._mqttclient = mqtt.Client(
                callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
                client_id=str(self._config._deviceID),
                transport='websockets',
                protocol=MQTTv5)
            self._mqttclient.username_pw_set(
                username=str(self._config._deviceID),
                password=self._config.connection_key)
            self.on_connect = config.on_connect
            self.on_disconnect = config.on_disconnect
            self.on_command = config.on_command
            self.on_vsupdate = config.on_vsupdate
            self._mqttclient.on_connect = self._onconnect_handler
            self._mqttclient.on_disconnect = self._ondisconnect_handler
            # self._mqttclient.on_message = self.onmessage_handler
            self._mqttclient._connect_timeout = 1.0
            self._transactions = Transactions()
            # Set TLS Context
            context = SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.load_verify_locations(cadata=ANEDYA_CA_CERTS)
            # self._mqttclient.tls_set()
            self._mqttclient.tls_set_context(context)
        else:
            self._mqttclient = None
        self._httpsession = requests.Session()
        # Base URL setup
        self._baseurl = "device." + self._config.region + ".anedya.io"
        headers = {'Content-type': 'application/json',
                   'Auth-mode': self._config.authmode,
                   'Authorization': self._config.connection_key}
        self._httpsession.headers.update(headers)
        return

    def set_config(self, config: AnedyaConfig):
        """
        Initialize the Anedya SDK.

        Args:
            config (AnedyaConfig): Anedya SDK configuration.
        """
        if config.connection_key == "":
            raise AnedyaInvalidConfig(
                'Configuration: connection key can not be empty!')
        if config._deviceid_set is False:
            raise AnedyaInvalidConfig(
                'Configuration: need to set a valid Device ID')
        self._config = config
        return

    def connect(self):
        if self._config.connection_mode == ConnectionMode.HTTP:
            raise AnedyaInvalidConfig(
                'Connection mode is HTTP, connect is not supported')
        if self._config.mqtt_mode == MQTTMode.TCP:
            print(self._mqttclient)
            self._mqttclient.loop_start()
            print("device." + self._config.region + ".anedya.io")
            err = self._mqttclient.connect(
                host="device.ap-in-1.anedya.io", port=8804,
                keepalive=60)
            print(err)
        # Start the loop

    def disconnect(self):
        self._mqttclient.disconnect()
        return

    from .client.bindDevice import bind_device
    from .client.submitData import submit_data
    from .client.submitLogs import submit_logs
    from .client.commandsUpdate import update_command_status
    from .client.commandsNext import next_command
    from .client.timeSync import get_time
    from .client.mqttHandlers import _onconnect_handler, _ondisconnect_handler
    from .client.callbacks import _error_callback, _response_callback, _command_callback, _vsupdate_callback
