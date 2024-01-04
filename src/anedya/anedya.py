import requests
from .config import *
from .store import *

class AnedyaClient:
    def set_config(self, config: AnedyaConfig):
        """
        Initialize the Anedya SDK.

        Args:
            config (AnedyaConfig): Anedya SDK configuration.
        """
        if config.connection_key == "":
            raise ValueError('Configuration: connection key can not be empty!')
        if config._deviceid_set == False:
            raise ValueError('Configuration: need to set a valid Device ID')
        self._config = config
        # Create 
        

    def submit_data(self, d: batch):
        """
        Send data to Anedya Cloud
        """
        headers = {'Content-type': 'application/json', 'Auth-mode': self._config.authmode, 'Authorization' : self._config.connection_key}
        if self._config._testmode :
            url = "https://device.stageapi.anedya.io/v1/submitData"
        else:
            url = "https://device." + self._config.region + ".anedya.io/v1/submitData"
        r = requests.post(url, data=d.encodeJSON(), headers=headers)
        #print(r.json())
        if r.status_code != 200:
            jsonResponse = r.json()
            print(jsonResponse)
            return False
        return True