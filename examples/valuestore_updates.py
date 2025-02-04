import anedya
import time

# Set the ID of the physical device
deviceID = "PHYSICAL_DEVICE_ID"
# Set the connection key for the device
connectionKey = "CONNECTION_KEY"


def main():
    config = anedya.default_config()
    config.connection_mode = anedya.ConnectionMode.MQTT
    config.set_deviceid(deviceID)
    config.set_connection_key(connectionKey)
    config.set_on_vsupdate(callback=on_VSUpdate_callback)

    # Create a client
    client = anedya.AnedyaClient(config)

    time.sleep(1)
    # Client is created, now connect with the MQTT server
    client.connect()
    time.sleep(2)

    input("Press Enter to continue after sending command...\n")
    print("Disconnecting")
    client.disconnect()


def on_VSUpdate_callback(vs):
    print(f"Received VS updates from platform!")
    print(f"Namespace: {vs.namespace}, Type: {vs.type}, Key: {vs.key}, Value: {vs.value}, Modified: {vs.modified}")
    return

if __name__ == '__main__':
    main()
