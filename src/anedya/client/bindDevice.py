import json
from ..config import ConnectionMode
from ..errors import AnedyaInvalidConfig, AnedyaTxFailure


def bind_device(self, binding_secret: str, timeout: float | None = None) -> bool:
    """
    Call this function to bind a device with the Anedya platform

    Args:
        binding_secret (str): A one time Binding secret obtained from the platform. This secret is usually passed to device during provisioning process through
        mobile app or any other process.
        timeout (float | None, optional): Time out in seconds for the request. In production setup it is advisable to use a timeout or else your program can get stuck indefinitely. Defaults to None.

    Raises:
        AnedyaInvalidConfig: Method can raise this method if either configuration is not provided or if the connection mode is invalid.
        AnedyaTxFailure: Method can raise this method if the transaction fails.

    Returns:
        bool: Returns true if the device is successfully bound with the platform.
    """
    if self._config is None:
        raise AnedyaInvalidConfig('Configuration not provided')
    if self._config.connection_mode == ConnectionMode.MQTT:
        return _bind_device_mqtt(self, binding_secret=binding_secret, timeout=timeout)
    elif self._config.connection_mode == ConnectionMode.HTTP:
        return _bind_device_http(self, binding_secret=binding_secret, timeout=timeout)
    else:
        raise AnedyaInvalidConfig('Invalid connection mode')


def _bind_device_http(self, binding_secret: str, timeout: float | None = None) -> bool:
    if self._config._testmode:
        url = "https://device.stageapi.anedya.io/v1/submitData"
    else:
        url = self._baseurl + "v1/bindDevice"
    requestPayload = {"bindingsecret": binding_secret,
                      "deviceid": str(self._config._deviceID)}
    r = self._httpsession.post(url, data=json.dumps(requestPayload), timeout=timeout)
    try:
        jsonResponse = r.json()
        payload = json.loads(jsonResponse)
        if payload['success'] is not True:
            raise AnedyaTxFailure(payload['error'], payload['errorcode'])
    except ValueError:
        raise AnedyaTxFailure(message="Invalid JSON response")
    return True


def _bind_device_mqtt(self, binding_secret: str, timeout: float | None = None):
    # Create and register a transaction
    tr = self._transactions.create_transaction()
    # Encode the payload
    requestPayload = {
        "reqId": tr.get_id(),
        "bindingsecret": binding_secret,
        "deviceid": str(self._config._deviceID)}
    payload = json.dumps(requestPayload)
    # Publish the message
    topic_prefix = "$anedya/device/" + str(self._config._deviceID)
    msginfo = self._mqttclient.publish(topic=topic_prefix + "/bindDevice/json",
                                       payload=payload, qos=1)
    try:
        msginfo.wait_for_publish(timeout=timeout)
    except ValueError:
        raise AnedyaTxFailure(message="Publish queue full")
    except RuntimeError as err:
        raise AnedyaTxFailure(message=str(err))
    # Wait for transaction to complete
    tr.wait_to_complete()
    # Transaction completed
    # Get the data from the transaction
    data = tr.get_data()
    # Clear transaction
    self._transactions.clear_transaction(tr)
    # Check if transaction is successful or not
    if data['success'] is not True:
        raise AnedyaTxFailure(data['error'], data['errorcode'])
    return
