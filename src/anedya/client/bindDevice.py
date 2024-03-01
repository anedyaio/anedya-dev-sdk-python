import requests
import json
from ..config import ConnectionMode


def bind_device(self, binding_secret: str):
    """
    Bind device to Anedya Cloud
    """
    if self._config.connection_mode == ConnectionMode.MQTT:
        result = _bind_device_mqtt(self, binding_secret)
    elif self._config.connection_mode == ConnectionMode.HTTP:
        result = _bind_device_http(self, binding_secret)
    return result


def _bind_device_mqtt(self, binding_secret: str):
    return


def _bind_device_http(self, binding_secret: str):
    headers = {'Content-type': 'application/json',
               'Auth-mode': self._config.authmode,
               'Authorization': self._config.connection_key}
    if self._config._testmode:
        url = "https://device.stageapi.anedya.io/v1/bindDevice"
    else:
        url = self._baseurl + "/v1/bindDevice/json"
    requestPayload = {"bindingsecret": binding_secret,
                      "deviceid": str(self._config._deviceID)}
    r = requests.post(url, data=json.dumps(requestPayload), headers=headers)
    jsonResponse = r.json()
    if r.status_code != 200:
        raise RuntimeError(jsonResponse)
    # Check whether the call was successful or not
    if jsonResponse["success"] is not True:
        raise Exception(jsonResponse)
    # Check whether the call was successful or not
    if jsonResponse["success"] is not True:
        raise Exception(jsonResponse)
    return True
