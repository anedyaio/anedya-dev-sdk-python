import time
import json
import requests


def get_time(self):
    """
    Get current time from Anedya Time Service using HTTP request - Gets current time using HTTP requests.
    Accuracy is generally within few tens of millisecond. For greater accuracy consider using NTP time service from Anedya
    """
    # print("called time API")
    if self._config._testmode:
        url = "https://device.stageapi.anedya.io/v1/time"
    else:
        url = "https://device." + self._config.region + ".anedya.io/v1/time"
    deviceSendTime = int(time.time_ns() / 1000000)
    requestPayload = {"deviceSendTime": deviceSendTime}
    # print(json.dumps(requestPayload))
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(requestPayload), headers=headers)
    deviceRecTime = int(time.time_ns() / 1000000)
    jsonResponse = r.json()
    # print(jsonResponse)
    if r.status_code != 200:
        raise Exception(jsonResponse)
    # Now compute the time from response
    ServerReceiveTime = jsonResponse["serverReceiveTime"]
    ServerSendTime = jsonResponse["serverSendTime"]
    currentTime = (ServerReceiveTime + ServerSendTime + deviceRecTime - deviceSendTime) / 2
    return currentTime
