import anedya
import time
import random

# Emulate Hardware Sensor?
virtual_sensor = True
# Set the ID of the physical device
deviceID = "773a6f34-db8d-48b4-8c09-fb728aec7c12"
# Set the connection key for the device
connectionKey = "03cdf9928841ec3315d699ac9dfb224c"

# Note: It is assumed that the humidity sensor is attached at GPIO23 of the Raspberry Pi

if not virtual_sensor:
    import board
    import adafruit_dht
    import psutil


def main():
    # Create a configuration object
    config = anedya.default_config()
    config.connection_mode = anedya.ConnectionMode.MQTT
    # Set the config parameters
    config.set_deviceid(deviceID)
    config.set_connection_key(connectionKey)

    # Create a client
    client = anedya.AnedyaClient(config)

    time.sleep(1)
    # Client is created, now connect with the MQTT server
    client.connect()
  
    time.sleep(2)
    print(client._mqttclient.is_connected())

    if not virtual_sensor:
        for proc in psutil.process_iter():
            if proc.name() == "libgpiod_pulsein" or proc.name() == "libgpiod_pulsei":
                proc.kill()
        sensor = adafruit_dht.DHT11(board.D23)

    while True:
        # Fetch data from the sensor
        print("Fetching data from the sensor")
        # Publish the datapoint
        data = anedya.DataPoints()
        # TODO
        if not virtual_sensor:
            try:
                temperature = sensor.temperature
                humidity = sensor.humidity
                # print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
            except RuntimeError as error:
                print(error.args[0])
                time.sleep(2.0)
                continue
            except Exception as error:
                sensor.exit()
                raise error
        else:
            temperature = 23 + (
                random.randrange(start=-5, stop=5, step=1) / 10
            )  # Assign static value in case of virtual sensor
            humidity = 63 + (
                random.randrange(start=-10, stop=10, step=1) / 10
            )  # Assign static value in case of virtual sensor
        print("Temperature: {t}C Humidity:{h}%".format(t=temperature, h=humidity))
        # Create an Anedya Datapoint object
        # Note that the timestamp needs to be in Milliseconds
        # variable filed requires the identifiers provided during variable creation
        dp1 = anedya.FloatData(
            variable="temperature",
            timestamp_milli=int(time.time_ns() / 1000000),
            value=temperature,
        )
        dp2 = anedya.FloatData(
            variable="humidity",
            timestamp_milli=int(time.time_ns() / 1000000),
            value=humidity,
        )

        # Append the data in a data store.
        data.append(dp1)
        data.append(dp2)

        client.submit_data(data)
        print("Data Pushed!")
        data.reset_datapoints()
        time.sleep(15)

    client.disconnect()


if __name__ == "__main__":
    main()
