import json
import string
import random
import base64
from ..models import CommandDetails, AnedyaEncoder
from ..transaction import Transaction
from ..errors import AnedyaInvalidConfig, AnedyaInvalidType, AnedyaTxFailure
from ..config import ConnectionMode
from ..models import CommandStatus


def update_command_status(self, command: CommandDetails, status: CommandStatus, ackdata: str | bytes | None = None, acktype: str = "string", timeout: float | None = None, callback_mode: bool = False) -> None | Transaction:
    """
    Update status of a command. Not thread safe.

    Args:
        command (CommandDetails): Command object of which status needs to be updated
        status (CommandStatus): New status of the command
        ackdata (str | bytes | None, optional): Data to be submitted along with acknowledgement. Maximum 1 kB of data is allowed. Defaults to None.
        acktype (str, optional): Specify the type of data submitted. Defaults to "string".
        timeout (float | None, optional): Time out in seconds for the request. In production setup it is advisable to use a timeout or else your program can get stuck indefinitely. Defaults to None.
        callback_mode (bool, optional): When using MQTT connection, it is not possible to publish the message from inside a callback. In such scenario, you can set callback_mode to True. Instead of publishing request right away, the function
        schedules the message to be published after the callback is completed. Also function returns a transaction object. Which can be used to check whether transaction has finished or not and what is the status of transaction.
        Use this method only when only single transaction is happening at a time. In the case where multiple transactions happening simultaneously, we suggest avoiding call to this function from within callback.Defaults to False.

    Raises:
        AnedyaInvalidConfig: Invalid configuration
        AnedyaInvalidType: Invalid datatype is specified
        AnedyaTxFailure: Transaction failure

    Returns:
        None | Transaction: Returns transaction object if callback_mode is True. returns None otherwise
    """
    if self._config is None:
        raise AnedyaInvalidConfig('Configuration not provided')
    if self._config.connection_mode == ConnectionMode.HTTP:
        return _update_command_status_http(self, command=command, status=status, timeout=timeout)
    elif self._config.connection_mode == ConnectionMode.MQTT:
        return _update_command_status_mqtt(self, command=command, status=status, timeout=timeout, callback_mode=callback_mode)
    else:
        raise AnedyaInvalidConfig('Invalid connection mode')


def _update_command_status_http(self, command: CommandDetails, status: CommandStatus, ackdata: str | bytes | None = None, acktype: str = "string", timeout: float | None = None) -> None:
    if self._config._testmode:
        url = "https://device.stageapi.anedya.io/v1/submitData"
    else:
        url = self._baseurl + "/v1/submitData"
    d = _UpdateCommandStatusReq("req_" + ''.join(random.choices(string.ascii_letters + string.digits, k=16)), command=command, status=status, ackdata=ackdata, acktype=acktype)
    r = self._httpsession.post(url, data=d.encodeJSON(), timeout=timeout)
    # print(r.json())
    try:
        jsonResponse = r.json()
        payload = json.loads(jsonResponse)
        if payload['success'] is not True:
            raise AnedyaTxFailure(payload['error'], payload['errorcode'])
    except ValueError:
        raise AnedyaTxFailure(message="Invalid JSON response")
    return


def _update_command_status_mqtt(self, command: CommandDetails, status: CommandStatus, ackdata: str | bytes | None = None, acktype: str = "string", timeout: float | None = None, callback_mode: bool = False) -> None:
    # Create and register a transaction
    tr = self._transactions.create_transaction()
    # Encode the payload
    d = _UpdateCommandStatusReq(tr.get_id(), command=command, status=status, ackdata=ackdata, acktype=acktype)
    payload = d.encodeJSON()
    # Publish the message
    print(payload)
    topic_prefix = "$anedya/device/" + str(self._config._deviceID)
    print(topic_prefix + "/commands/updateStatus/json")
    msginfo = self._mqttclient.publish(topic=topic_prefix + "/commands/updateStatus/json",
                                       payload=payload, qos=1)
    if callback_mode:
        # Can not block in callback mode
        return tr
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
    return


class _UpdateCommandStatusReq:
    def __init__(self, reqId: str, command: CommandDetails, status: CommandStatus, ackdata: str | bytes | None = None, acktype: str = "string"):
        self.command_id = command.id
        self.reqID = reqId
        self.status = status
        if acktype == "string":
            if isinstance(ackdata, str):
                raise AnedyaInvalidType('ackdata is not a valid str')
            self.ackdata = ackdata
            self.acktype = "string"
        elif acktype == "binary":
            if isinstance(ackdata, bytes):
                raise AnedyaInvalidType('ackdata is not a valid list')
            self.ackdata_binary = ackdata
            self.ackdata = base64.b64encode(self.ackdata_binary).decode('ascii')
            self.acktype = "binary"
        else:
            raise AnedyaInvalidType('Invalid acktype')
        if ackdata is None:
            self.ackdata = ""
            self.acktype = "string"

    def toJSON(self):
        dict = {
            "reqId": self.reqID,
            "commandId": str(self.command_id),
            "status": self.status,
            "ackdata": self.ackdata,
            "ackdatatype": self.acktype
        }
        return dict

    def encodeJSON(self):
        data = json.dumps(self, cls=AnedyaEncoder)
        return data
