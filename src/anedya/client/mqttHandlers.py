from ..errors import AnedyaInvalidCredentials, AnedyaRateLimitExceeded
from ..errors import AnedyaException


def _onconnect_handler(self, client, userdata, flags, reason_code, properties):
    rc = reason_code.value
    if rc == 135:
        raise AnedyaInvalidCredentials("Invalid credentials")
    elif rc == 134:
        raise AnedyaInvalidCredentials("Invalid Credentials")
    elif rc == 159:
        raise AnedyaRateLimitExceeded("Connection rate exceeded")
    if rc != 0:
        raise AnedyaException(
            f"Connection failed with reason code {reason_code.getName()}")
    if rc == 0:
        topic_prefix = "$anedya/device/" + str(self._config._deviceID)
        # Connection is successful, subscribe to the error and response topics.
        self._mqttclient.subscribe(
            topic=topic_prefix + "/errors", qos=0)
        self._mqttclient.subscribe(
            topic=topic_prefix + "/response", qos=0)
        self._mqttclient.subscribe(
            topic=topic_prefix + "/commands", qos=0)
        self._mqttclient.subscribe(
            topic=topic_prefix + "/valuestore/updates/json", qos=0)
        # Define all Callbacks for error and response
        # Callback for errors
        print("Adding Callbacks")
        self._mqttclient.message_callback_add(sub=topic_prefix + "/errors", callback=self._error_callback)
        # Callback for response
        self._mqttclient.message_callback_add(sub=topic_prefix + "/response", callback=self._response_callback)
        # Callback for command
        self._mqttclient.message_callback_add(sub=topic_prefix + "/commands", callback=self._command_callback)
        # Callback for valuestore updates
        self._mqttclient.message_callback_add(sub=topic_prefix + "/valuestore/updates/json", callback=self._vsupdate_callback)
        # Call the on_connect callback if it is not None
        if self.on_connect is not None:
            self.on_connect()
    return


def _ondisconnect_handler(self,
                          client,
                          userdata,
                          disconnect_flags,
                          reason_code,
                          properties):
    # First call the disconnect handler callback
    if self.on_disconnect is not None:
        self.on_disconnect(client,
                           userdata,
                           disconnect_flags,
                           reason_code,
                           properties)
    # Retry connecting
    self._mqttclient.reconnect()
    return
