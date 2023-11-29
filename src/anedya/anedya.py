import requests
from .config import *
from .store import *

class AnedyaClient:
    def SetConfig(self, config: AnedyaConfig):
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
        r = requests.post("https://device." + self._config.region + ".anedya.io/v1/submitData", data=d.encodeJSON(), headers=headers)
        #print(r.json())
        if r.status_code != 200:
            jsonResponse = r.json()
            print(jsonResponse)
            return False
        return True