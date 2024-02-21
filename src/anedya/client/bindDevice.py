import requests
import json


def bind_device(self, binding_secret: str):
    """
    Bind device to Anedya Cloud
    """
    headers = {'Content-type': 'application/json', 'Auth-mode': self._config.authmode, 'Authorization': self._config.connection_key}
    if self._config._testmode:
        url = "https://device.stageapi.anedya.io/v1/bindDevice"
    else:
        url = "https://device." + self._config.region + ".anedya.io/v1/bindDevice/json"
    requestPayload = {"bindingsecret": binding_secret, "deviceid": str(self._config._deviceID)}
    r = requests.post(url, data=json.dumps(requestPayload), headers=headers)
    jsonResponse = r.json()
    if r.status_code != 200:
        raise Exception(jsonResponse)
    # Check whether the call was successful or not
    if jsonResponse["success"] is not True:
        raise Exception(jsonResponse)
    return True
