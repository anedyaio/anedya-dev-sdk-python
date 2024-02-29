
def onconnect_handler(self, client, userdata, flags, reason_code, properties):
    if self.on_connect is not None:
        # Call the on_connect callback
        self.on_connect(client, userdata, flags, reason_code, properties)
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
