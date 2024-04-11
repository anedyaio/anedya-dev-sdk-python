from ..errors import AnedyaInvalidConfig, AnedyaTxFailure
from ..config import ConnectionMode
from ..models import DataPoints, SubmitDataMQTTReq
import json


def submit_data(self, data: DataPoints, timeout: float | None = None):
    """
    :param data: Data to send as a :class: DataPoints object
    :param timeout: Timeout in seconds, default is None

    :raises AnedyaTxFailure: If data could not be submitted due to an error

    This function sends data to the Anedya Cloud platform. It determines the connection mode from the SDK configuration and calls the appropriate submit data method (_submit_data_http or _submit_data_mqtt).
    """

    if self._config is None:
        raise AnedyaInvalidConfig('Configuration not provided')
    if self._config.connection_mode == ConnectionMode.HTTP:
        return _submit_data_http(self, data=data, timeout=timeout)
    elif self._config.connection_mode == ConnectionMode.MQTT:
        return _submit_data_mqtt(self, data=data, timeout=timeout)
    else:
        raise AnedyaInvalidConfig('Invalid connection mode')


def _submit_data_http(self, data: DataPoints, timeout: float | None = None):
    if self._config._testmode:
        url = "https://device.stageapi.anedya.io/v1/submitData"
    else:
        url = self._baseurl + "/v1/submitData"
    r = self._httpsession.post(url, data=data.encodeJSON(), timeout=timeout)
    # print(r.json())
    try:
        jsonResponse = r.json()
        payload = json.loads(jsonResponse)
        if payload['success'] is not True:
            raise AnedyaTxFailure(payload['error'], payload['errCode'])
    except ValueError:
        raise AnedyaTxFailure(message="Invalid JSON response")
    return


def _submit_data_mqtt(self, data: DataPoints, timeout: float | None = None):
    # Create and register a transaction
    tr = self._transactions.create_transaction()
    # Encode the payload
    d = SubmitDataMQTTReq(tr.get_id(), data)
    payload = d.encodeJSON()
    # Publish the message
    print(payload)
    topic_prefix = "$anedya/device/" + str(self._config._deviceID)
    print(topic_prefix + "/submitData/json")
    msginfo = self._mqttclient.publish(topic=topic_prefix + "/submitdata/json",
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
