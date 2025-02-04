from ..errors import AnedyaInvalidConfig, AnedyaTxFailure
from ..config import ConnectionMode
import json
import time


def get_time(self, timeout: float | None = None) -> int:
    """
    Fetch the time information from Anedya.

    Args:
        timeout (float | None, optional): Time out in seconds for the request. In production setup it is advisable to use a timeout or else your program can get stuck indefinitely. Defaults to None.

    Raises:
        AnedyaInvalidConfig: Method can raise this method if either configuration is not provided or if the connection mode is invalid.
        AnedyaTxFailure: Method can raise this method if the transaction fails.

    Returns:
        int: The method returns the current time in Unix millisecond epoch in UTC timezone
    """
    if self._config is None:
        raise AnedyaInvalidConfig('Configuration not provided')
    if self._config.connection_mode == ConnectionMode.HTTP:
        return _time_sync_http(self, timeout=timeout)
    elif self._config.connection_mode == ConnectionMode.MQTT:
        return _time_sync_mqtt(self, timeout=timeout)
    else:
        raise AnedyaInvalidConfig('Invalid connection mode')


def _time_sync_http(self, timeout: float | None = None):
    # print("called time API")
    if self._config._testmode:
        url = "https://device.stageapi.anedya.io/v1/time"
    else:
        url = "https://device." + self._config.region + ".anedya.io/v1/time"
    deviceSendTime = int(time.time_ns() / 1000000)
    requestPayload = {"deviceSendTime": deviceSendTime}
    r = self._httpsession.post(url, data=json.dumps(requestPayload), timeout=timeout)
    try:
        jsonResponse = r.json()
        payload = json.loads(jsonResponse)
        if payload['success'] is not True:
            raise AnedyaTxFailure(payload['error'], payload['errorcode'])
        deviceRecTime = int(time.time_ns() / 1000000)
        ServerReceiveTime = int(jsonResponse["serverReceiveTime"])
        ServerSendTime = int(jsonResponse["serverSendTime"])
        currentTime = int((ServerReceiveTime + ServerSendTime + deviceRecTime - deviceSendTime) / 2)
    except ValueError:
        raise AnedyaTxFailure(message="Invalid JSON response")
    return currentTime


def _time_sync_mqtt(self, timeout: float | None = None):
    # Create and register a transaction
    tr = self._transactions.create_transaction()
    # Create the payload
    deviceSendTime = int(time.time_ns() / 1000000)
    requestPayload = {"deviceSendTime": deviceSendTime}
    payload = json.dumps(requestPayload)
    # Publish the message
    self._mqttclient.publish(topic="$anedya/device/" + str(self._config._deviceID) + "/getTime/json",
                             payload=payload, qos=1)
    # Wait for transaction to complete
    tr.wait_to_complete()
    deviceRecTime = int(time.time_ns() / 1000000)
    # Transaction completed
    # Get the data from the transaction
    data = tr.get_data()
    ServerReceiveTime = data["serverReceiveTime"]
    ServerSendTime = data["serverSendTime"]
    currentTime = (ServerReceiveTime + ServerSendTime + deviceRecTime - deviceSendTime) / 2
    # Decode the paylo
    return currentTime
