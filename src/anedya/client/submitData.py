from ..errors import AnedyaInvalidConfig, AnedyaTxFailure
from ..config import ConnectionMode
from ..models import DataPoints, AnedyaEncoder
import json


def submit_data(self, data: DataPoints, timeout: float | None = None):
    """
    Submit data to Anedya Platform.

    Args:
        data (DataPoints): Datapoints object, you can submit multiple types of variable in single request.
        timeout (float | None, optional): Time out in seconds for the request. In production setup it is advisable to use a timeout or else your program can get stuck indefinitely. Defaults to None.

    Raises:
        AnedyaInvalidConfig: Method can raise this method if either configuration is not provided or if the connection mode is invalid.
        AnedyaTxFailure: Method can raise this method if the transaction fails.
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
        url = "https://"+ self._baseurl + "/v1/submitData"
    r = self._httpsession.post(url, data=data.encodeJSON(), timeout=timeout)
    # print(r.json())
    try:
        payload = r.json()
        if payload['success'] is not True:
            raise AnedyaTxFailure(payload['error'], payload['errorcode'])
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
    # print(payload)
    topic_prefix = "$anedya/device/" + str(self._config._deviceID)
    # print(topic_prefix + "/submitData/json")
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
        raise AnedyaTxFailure(data['error'], data['errorcode'])
    return


class SubmitDataMQTTReq:
    def __init__(self, reqID: str, data: DataPoints):
        self.data = data
        self.reqID = reqID

    def toJSON(self):
        dict = {
            "reqId": self.reqID,
            "data": self.data.data
        }
        return dict

    def encodeJSON(self):
        data = json.dumps(self, cls=AnedyaEncoder)
        return data
