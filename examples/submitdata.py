import anedya
import time
import board
import adafruit_dht
import psutil

# Set the ID of the device
deviceID = '165ba802-8ea6-11ee-ba2e-57c37d9f47c1'
# Set the connection key for the device
connectionKey = 'cff8805084df2cc2159af5e230b155f7'

def main():
    # Create a configuration object
    config = anedya.default_config()
    # Set the config parameters
    config.setdeviceid(deviceID)
    config.setconnection_key(connectionKey)

    # Configuration has been set, create an Anedya Client Instance
    client = anedya.AnedyaClient()
    client.SetConfig(config)

    data = anedya.batch()

    # Client is set, now we can start collecting data

    for proc in psutil.process_iter():
        if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
           proc.kill()
    sensor = adafruit_dht.DHT11(board.D23)

    while True:
        # Fetch data from the sensor
        print('Fetching data from the sensor')
        # TODO
        try:
            temperature = sensor.temperature
            humidity = sensor.humidity
            #print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            sensor.exit()
            raise error
        print('Temperature: {t}C Humidity: {h}%'.format(t=temperature, h=humidity))
        # Create an Anedya Datapoint object
        dp1 = anedya.FloatData(name='temperature', timestamp=int(time.time()), value=temperature)
        dp2 = anedya.FloatData(name='humidity', timestamp=int(time.time()), value=humidity)

        # Append the data in a data store.
        data.append(dp1)
        data.append(dp2)

        # Submit the data to the Anedya Platform
        success = client.submit_data(data)
        if success:
            print('Data pushed to Anedya Cloud!')
        else:
            print('Error pushing data to the cloud!')
        # Clear all the data in the store before proceeding to next
        data.reset_datapoints()
        time.sleep(15)        

if __name__ == "__main__":
    main()