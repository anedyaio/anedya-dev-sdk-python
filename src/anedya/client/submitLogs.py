from ..models import LogsCache, AnedyaEncoder
from ..errors import AnedyaInvalidConfig, AnedyaTxFailure
from ..config import ConnectionMode
import json


def submit_logs(self, logs: LogsCache, timeout: float | None = None):
    """
    Submit logs to Anedya

    Args:
        logs (LogsCache): Logs
        timeout (float | None, optional): Time out in seconds for the request. In production setup it is advisable to use a timeout or else your program can get stuck indefinitely. Defaults to None.

    Raises:
        AnedyaInvalidConfig: Method can raise this method if either configuration is not provided or if the connection mode is invalid.
        AnedyaTxFailure: Method can raise this method if the transaction fails.
    """
    if self._config is None:
        raise AnedyaInvalidConfig('Configuration not provided')
    if self._config.connection_mode == ConnectionMode.HTTP:
        return _submit_log_http(self, logs=logs, timeout=timeout)
    elif self._config.connection_mode == ConnectionMode.MQTT:
        return _submit_log_mqtt(self, logs=logs, timeout=timeout)
    else:
        raise AnedyaInvalidConfig('Invalid connection mode')


def _submit_log_http(self, logs: LogsCache, timeout: float | None = None):
    if self._config._testmode:
        url = "https://device.stageapi.anedya.io/v1/logs/submitLogs"
    else:
        url = self._baseurl + "/v1/submitLogs"
    r = self._httpsession.post(url, data=logs.encodeJSON(), timeout=timeout)
    # print(r.json())
    try:
        jsonResponse = r.json()
        payload = json.loads(jsonResponse)
        if payload['success'] is not True:
            raise AnedyaTxFailure(payload['error'], payload['errorcode'])
    except ValueError:
        raise AnedyaTxFailure(message="Invalid JSON response")


def _submit_log_mqtt(self, data: LogsCache, timeout: float | None = None):
    # Create and register a transaction
    tr = self._transactions.create_transaction()
    # Encode the payload
    d = SubmitLogsMQTTReq(tr.get_id(), data)
    payload = d.encodeJSON()
    # Publish the message
    self._mqttclient.publish(topic="$anedya/device/" + str(self._config._deviceID) + "/submitLogs/json",
                             payload=payload, qos=1)
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


class SubmitLogsMQTTReq:
    def __init__(self, reqID: str, logs: LogsCache):
        self.logs = logs
        self.reqID = reqID

    def toJSON(self):
        dict = {
            "reqId": self.reqID,
            "data": self.logs.logs
        }
        return dict

    def encodeJSON(self):
        data = json.dumps(self, cls=AnedyaEncoder)
        return data
