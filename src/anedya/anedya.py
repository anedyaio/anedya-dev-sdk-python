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


class AnedyaClient:

    def __init__(self, config: AnedyaConfig):
        self.set_config(config)

        # Internal Parameters
        self._mqttclient = None
        return

    def set_config(self, config: AnedyaConfig):
        """
        Initialize the Anedya SDK.

        Args:
            config (AnedyaConfig): Anedya SDK configuration.
        """
        if config.connection_key == "":
            raise AnedyaInvalidConfig('Configuration: connection key can not be empty!')
        if config._deviceid_set is False:
            raise AnedyaInvalidConfig('Configuration: need to set a valid Device ID')
        self._config = config
        # Create

    from .client.bindDevice import bind_device
    from .client.submitData import submit_data
    from .client.timeSync import get_time
