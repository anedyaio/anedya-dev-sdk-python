import json
import time
import uuid
import base64
import datetime


class FloatData:
    def __init__(self, variable: str, value: float, timestamp_milli: int = int(time.time_ns() / 1000000)):
        """
        Create a Float datapoint object which can be sent to Anedya Server

        Args:
            variable (str): Name of the variable
            value (float): Value of the variable
            timestamp_milli (int, optional): Timestamp in millisecond unix epoch. Defaults to current time. Pass 0 to take Anedya Server Time
        """
        self.variable = variable
        self.timestamp = timestamp_milli
        self.value = value

    def toJSON(self):
        dict = {
            "variable": self.variable,
            "timestamp": self.timestamp,
            "value": self.value
        }
        return dict


class Log:
    def __init__(self, log: str, timestamp_milli: int = int(time.time_ns() / 1000000)):
        """
        Create a Log object which can be sent to Anedya Server

        Args:
            log (str): Log string that you want to send to Anedya
            timestamp_milli (int, optional): Timestamp in millisecond unix epoch. Defaults to current time. Pass 0 to take Anedya Server Time
        """
        self.log = log
        self.timestamp = timestamp_milli

    def toJSON(self):
        dict = {
            "log": self.log,
            "timestamp": self.timestamp
        }
        return dict


class DataPoints:
    def __init__(self):
        self.data = []

    def append(self, datapoint: FloatData):
        """
        Append a datapoint to the datapoints batch which will be sent to Anedya Server in a single request

        Args:
            datapoint (FloatData): Datapoint object
        """
        self.data.append(datapoint)

    def toJSON(self):
        dict = {
            "data": self.data
        }
        return dict

    def reset_datapoints(self):
        self.data = []

    def encodeJSON(self):
        data = json.dumps(self, cls=AnedyaEncoder)
        return data


class LogsCache:
    def __init__(self):
        self.logs = []

    def append(self, log: Log):
        """
        Append a log to the log batch which will be sent to Anedya Server in a single request

        Args:
            log (Log): Log object
        """
        self.logs.append(log)

    def toJSON(self):
        dict = {
            "data": self.logs
        }
        return dict

    def reset_logs(self):
        self.logs = []

    def encodeJSON(self):
        data = json.dumps(self, cls=AnedyaEncoder)
        return data


class CommandMessage:
    def __init__(self, commandMsg: dict):
        self.command = commandMsg["command"]
        self.id = uuid.UUID(commandMsg["id"])
        if type == "string":
            self.data = commandMsg["data"]
        elif type == "binary":
            base64_bytes = commandMsg["data"].encode("ascii")
            data_bytes = base64.b64decode(base64_bytes)
            self.data = data_bytes
        else:
            raise Exception("Invalid datatype")
        self.type = commandMsg["type"]
        self.exp = datetime.datetime.fromtimestamp(commandMsg["exp"] / 1000)


class AnedyaEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'toJSON'):
            return obj.toJSON()
        else:
            return json.JSONEncoder.default(self, obj)
