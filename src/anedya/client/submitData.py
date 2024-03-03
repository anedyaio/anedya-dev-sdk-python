from ..errors import AnedyaInvalidConfig
from ..config import ConnectionMode
from ..models import DataPoints, SubmitDataMQTTReq


def submit_data(self, data: DataPoints):
    """
    Send data to Anedya Cloud
    """
    if self._config is None:
        raise AnedyaInvalidConfig('Configuration not provided')
    if self._config.connection_mode == ConnectionMode.HTTP:
        return _submit_data_http(self, data)
    elif self._config.connection_mode == ConnectionMode.MQTT:
        return _submit_data_mqtt(self, data)
    else:
        raise AnedyaInvalidConfig('Invalid connection mode')


def _submit_data_http(self, data: DataPoints):
    """
    Send data to Anedya Cloud
    """
    if self._config._testmode:
        url = "https://device.stageapi.anedya.io/v1/submitData"
    else:
        url = self._baseurl + "/v1/submitData"
    r = self._httpsession.post(url, data=data.encodeJSON())
    # print(r.json())
    if r.status_code != 200:
        jsonResponse = r.json()
        print(jsonResponse)
        return False
    return True


def _submit_data_mqtt(self, data: DataPoints):
    """
    Send data to Anedya Cloud through MQTT
    """
    # Create and register a transaction
    tr = self._transactions.create_transaction()
    # Encode the payload
    d = SubmitDataMQTTReq(tr.get_id(), data)
    payload = d.encodeJSON()
    # Publish the message
    topic_prefix = "$anedya/device/" + str(self._config._deviceID)
    self._mqttclient.publish(topic=topic_prefix + "/submitData/json",
                             payload=payload, qos=1)
    # Wait for transaction to complete

    # Clear transaction
    return
