from ..errors import AnedyaInvalidConfig, AnedyaInvalidProtocol
from ..config import ConnectionMode
from ..store import DataPoints
import requests


def submit_data(self, data: DataPoints):
    """
    Send data to Anedya Cloud
    """
    if self._config is None:
        raise AnedyaInvalidConfig('Configuration not provided')
    if self._config.connection_mode != ConnectionMode.HTTP:
        raise AnedyaInvalidProtocol('This function should not be called connection mode is not HTTPS')
    headers = {'Content-type': 'application/json', 'Auth-mode': self._config.authmode, 'Authorization': self._config.connection_key}
    if self._config._testmode:
        url = "https://device.stageapi.anedya.io/v1/submitData"
    else:
        url = "https://device." + self._config.region + ".anedya.io/v1/submitData"
    r = requests.post(url, data=data.encodeJSON(), headers=headers)
    # print(r.json())
    if r.status_code != 200:
        jsonResponse = r.json()
        print(jsonResponse)
        return False
    return True
