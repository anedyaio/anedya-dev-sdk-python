from ..errors import AnedyaInvalidCredentials, AnedyaRateLimitExceeded
from ..errors import AnedyaException


def onconnect_handler(self, client, userdata, flags, reason_code, properties):
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
    if self.on_connected is not None and rc == 0:
        # Call the on_connect callback
        self.on_connected()
    return


def ondisconnect_handler(self,
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
