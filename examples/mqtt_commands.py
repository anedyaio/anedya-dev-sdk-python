import anedya
import time

client = None
tr = None

# Set the ID of the physical device
deviceID = "<PHYSICAL-DEVICE-ID>"
# Set the connection key for the device
connectionKey = "<NODE-CONNECTION-KEY>"


def main():
    config = anedya.default_config()
    config.connection_mode = anedya.ConnectionMode.MQTT
    config.set_deviceid(deviceID)
    config.set_connection_key(connectionKey)
    config.set_on_command(callback=on_command_callback)

    # Create a client
    global client
    client = anedya.AnedyaClient(config)

    time.sleep(1)
    # Client is created, now connect with the MQTT server
    client.connect()
    time.sleep(2)
    print(client._mqttclient.is_connected())

    # Publish the datapoint

    input("Press Enter to continue after sending command...")
    tr.wait_to_complete()
    print("Disconnecting")
    client.disconnect()


def on_command_callback(cmdinput: anedya.CommandDetails):
    print(f"Received command from platform: {cmdinput.command}")
    # Change the status of the command
    global tr
    tr = client.update_command_status(command=cmdinput, status=anedya.CommandStatus.RECEIVED, callback_mode=True)
    return


if __name__ == '__main__':
    main()
