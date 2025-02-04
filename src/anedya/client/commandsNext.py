from ..models import CommandDetails, AnedyaEncoder
from ..config import ConnectionMode
from ..errors import AnedyaTxFailure, AnedyaInvalidConfig
import uuid
import json
import base64
import random
import string
import datetime


def next_command(self, timeout: float | None = None) -> tuple[CommandDetails, bool]:
    """
    Get the next command from the server.
    Returns:
        CommandDetails: The next command.

    Raises:
        AnedyaTxFailure: If the transaction fails.
    """
    if self._config is None:
        raise AnedyaInvalidConfig('Configuration not provided')
    if self._config.connection_mode == ConnectionMode.HTTP:
        return _next_command_http(self, timeout=timeout)
    elif self._config.connection_mode == ConnectionMode.MQTT:
        return _next_command_mqtt(self, timeout=timeout)
    else:
        raise AnedyaInvalidConfig('Invalid connection mode')


def _next_command_http(self, timeout: float | None = None) -> tuple[CommandDetails, bool]:
    if self._config._testmode:
        url = "https://device.stageapi.anedya.io/v1/submitData"
    else:
        url = self._baseurl + "/v1/submitData"
    d = _next_command_req("req_" + ''.join(random.choices(string.ascii_letters + string.digits, k=16)))
    r = self._httpsession.post(url, data=d.encodeJSON(), timeout=timeout)
    # print(r.json())
    try:
        jsonResponse = r.json()
        payload = json.loads(jsonResponse)
        if payload['success'] is not True:
            raise AnedyaTxFailure(payload['error'], payload['errorcode'])
        # Payload has success now create a CommandDetails object and return
        command = CommandDetails()
        command.id = uuid.UUID(payload["commandId"])
        command.command = payload["command"]
        command.status = payload["status"]
        command.type = payload["datatype"]
        if self.type == "string":
            self.data = payload["data"]
        elif self.type == "binary":
            base64_bytes = payload["data"].encode("ascii")
            data_bytes = base64.b64decode(base64_bytes)
            self.data = data_bytes
        command.updated = datetime.datetime.fromtimestamp(payload["updated"] / 1000)
        command.issued = datetime.datetime.fromtimestamp(payload["issued"] / 1000)
    except ValueError:
        raise AnedyaTxFailure(message="Invalid JSON response")
    return command, payload['nextavailable']


def _next_command_mqtt(self, timeout: float | None = None) -> tuple[CommandDetails, bool]:
    # Create and register a transaction
    tr = self._transactions.create_transaction()
    # Encode the payload
    d = _next_command_req(tr.get_id())
    payload = d.encodeJSON()
    # Publish the message
    print(payload)
    topic_prefix = "$anedya/device/" + str(self._config._deviceID)
    print(topic_prefix + "/commands/updateStatus/json")
    msginfo = self._mqttclient.publish(topic=topic_prefix + "/commands/updateStatus/json",
                                       payload=payload, qos=1)
    try:
        msginfo.wait_for_publish(timeout=timeout)
    except ValueError:
        raise AnedyaTxFailure(message="Publish queue full")
    except RuntimeError as err:
        raise AnedyaTxFailure(message=str(err))
    except Exception as err:
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
    try:
        if data['available'] is not True:
            return None, None
        command = CommandDetails()
        command.id = uuid.UUID(payload["commandId"])
        command.command = payload["command"]
        command.status = payload["status"]
        command.type = payload["datatype"]
        if self.type == "string":
            self.data = payload["data"]
        elif self.type == "binary":
            base64_bytes = payload["data"].encode("ascii")
            data_bytes = base64.b64decode(base64_bytes)
            self.data = data_bytes
        command.updated = datetime.datetime.fromtimestamp(payload["updated"] / 1000)
        command.issued = datetime.datetime.fromtimestamp(payload["issued"] / 1000)
    except ValueError:
        raise AnedyaTxFailure(message="Invalid JSON response")
    return command, payload['nextavailable']


class _next_command_req:
    def __init__(self, req_id: str):
        self.reqID = req_id
        return

    def toJSON(self):
        dict = {
            "reqId": self.reqID,
        }
        return dict

    def encodeJSON(self):
        data = json.dumps(self, cls=AnedyaEncoder)
        return data
