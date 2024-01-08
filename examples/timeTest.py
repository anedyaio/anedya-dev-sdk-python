import anedya
import time

config = anedya.default_config()
config.setdeviceid("667cdb30-dbbb-44a9-9925-f4f5dd223ea2")
config.setconnection_key("test")
config._testmode = True
client = anedya.AnedyaClient()
client.set_config(config)
t = client.get_time_http()
print(t)
print(time.time_ns()/1000000)
print(int(time.time_ns()/1000000) - t)
