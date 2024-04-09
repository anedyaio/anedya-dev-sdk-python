import anedya
import time

config = anedya.default_config()
config.connection_mode = anedya.ConnectionMode.MQTT
config.set_deviceid("<SET-DEVICE-ID>")
config.set_connection_key("<SET-CONNECTION-KEY>")

# Create a client
client = anedya.AnedyaClient(config)

time.sleep(1)
# Client is created, now connect with the MQTT server
client.connect()
time.sleep(2)
print(client._mqttclient.is_connected())

# Publish the datapoint
data = anedya.DataPoints()

dp1 = anedya.FloatData(variable='temperature', timestamp_milli=int(time.time_ns() / 1000000), value=10)

data.append(dp1)

client.submit_data(data)

time.sleep(10)
client.disconnect()
