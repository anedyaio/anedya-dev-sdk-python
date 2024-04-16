import json
from ..config import ConnectionMode
from ..errors import AnedyaInvalidConfig, AnedyaTxFailure


def bind_device(self, binding_secret: str, timeout: float | None = None):
    """
    :param binding_secret: Binding secret to be used for binding the device
    :raises AnedyaInvalidConfig: If the configuration is not provided
    :raises AnedyaTxFailure: If the transaction fails

    This function provides a way to bind a device to the Anedya platform.
    """
    if self._config is None:
        raise AnedyaInvalidConfig('Configuration not provided')
    if self._config.connection_mode == ConnectionMode.MQTT:
        return _bind_device_mqtt(self, binding_secret=binding_secret, timeout=timeout)
    elif self._config.connection_mode == ConnectionMode.HTTP:
        return _bind_device_http(self, binding_secret=binding_secret, timeout=timeout)
    else:
        raise AnedyaInvalidConfig('Invalid connection mode')


def _bind_device_http(self, binding_secret: str, timeout: float | None = None):
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
            raise AnedyaTxFailure(payload['error'], payload['errCode'])
    except ValueError:
        raise AnedyaTxFailure(message="Invalid JSON response")
    return


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
        raise AnedyaTxFailure(data['error'], data['errCode'])
    return
