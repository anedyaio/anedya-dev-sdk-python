import anedya
import time

config = anedya.default_config()
config.connection_mode = anedya.ConnectionMode.MQTT
config.set_deviceid("67719273-7cfe-4726-a846-72ca86340916")
config.set_connection_key("7346b841bc8cf7fe39555ae19654612c")

# Create a client
client = anedya.AnedyaClient(config)

time.sleep(1)
# Client is created, now connect with the MQTT server
client.connect()
time.sleep(2)
print(client._mqttclient.is_connected())
time.sleep(10)
client.disconnect()
