"""
    Copyright 2024 Anedya Systems Private Limited

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import requests
import time
import json
from .config import *
from .store import *

class AnedyaClient:

    def __init__(self, config: AnedyaConfig):
        self.set_config(config)
        return

    def set_config(self, config: AnedyaConfig):
        """
        Initialize the Anedya SDK.

        Args:
            config (AnedyaConfig): Anedya SDK configuration.
        """
        if config.connection_key == "":
            raise ValueError('Configuration: connection key can not be empty!')
        if config._deviceid_set == False:
            raise ValueError('Configuration: need to set a valid Device ID')
        self._config = config
        # Create 
        
    def bind_device(self, binding_secret: str):
        """
        Bind device to Anedya Cloud
        """
        headers = {'Content-type': 'application/json', 'Auth-mode': self._config.authmode, 'Authorization' : self._config.connection_key}
        if self._config._testmode :
            url = "https://device.stageapi.anedya.io/v1/submitData"
        else:
            url = "https://device." + self._config.region + ".anedya.io/v1/bindDevice/json"
        requestPayload = {"bindingsecret" : binding_secret, "deviceid" : str(self._config._deviceID)}
        r = requests.post(url, data=json.dumps(requestPayload), headers=headers)
        jsonResponse = r.json()
        if r.status_code != 200:
            raise Exception(jsonResponse)
        # Check whether the call was successful or not
        if jsonResponse["success"] != True:
            raise Exception(jsonResponse)
        return True
    
    def submit_data(self, d: batch):
        """
        Send data to Anedya Cloud
        """
        headers = {'Content-type': 'application/json', 'Auth-mode': self._config.authmode, 'Authorization' : self._config.connection_key}
        if self._config._testmode :
            url = "https://device.stageapi.anedya.io/v1/submitData"
        else:
            url = "https://device." + self._config.region + ".anedya.io/v1/submitData"
        r = requests.post(url, data=d.encodeJSON(), headers=headers)
        #print(r.json())
        if r.status_code != 200:
            jsonResponse = r.json()
            print(jsonResponse)
            return False
        return True
    
    def get_time_http(self):
        """
        Get current time from Anedya Time Service using HTTP request - Gets current time using HTTP requests.
        Accuracy is generally within few tens of millisecond. For greater accuracy consider using NTP time service from Anedya
        """
        #print("called time API")
        if self._config._testmode :
            url = "https://device.stageapi.anedya.io/v1/time"
        else:
            url = "https://device." + self._config.region + ".anedya.io/v1/time"
        deviceSendTime = int(time.time_ns()/1000000)
        requestPayload = {"deviceSendTime" : deviceSendTime}
        #print(json.dumps(requestPayload))
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(requestPayload), headers=headers)
        deviceRecTime = int(time.time_ns()/1000000)
        jsonResponse = r.json()
        #print(jsonResponse)
        if r.status_code != 200:
            raise Exception(jsonResponse)
        # Now compute the time from response
        ServerReceiveTime = jsonResponse["serverReceiveTime"]
        ServerSendTime = jsonResponse["serverSendTime"]
        currentTime = (ServerReceiveTime + ServerSendTime + deviceRecTime - deviceSendTime)/2
        return currentTime
        