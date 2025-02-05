import json
import time
import uuid
import base64
import datetime
from enum import Enum


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


class GeoData:
    def __init__(self, variable: str, lat: float, long: float, timestamp_milli: int = int(time.time_ns() / 1000000)):
        """
        Create a Geo datapoint object which can be sent to Anedya Server

        Args:
            variable (str): Name of the variable
            lat (float): Latitude of the location
            lon (float): Longitude of the location
            timestamp_milli (int, optional): Timestamp in millisecond unix epoch. Defaults to current time. Pass 0 to take Anedya Server Time
        """
        self.variable = variable
        self.timestamp = timestamp_milli
        self.lat = lat
        self.long = long

    def toJSON(self):
        dict = {
            "variable": self.variable,
            "timestamp": self.timestamp,
            "value": {
                "lat": self.lat,
                "long": self.long
            }
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


class CommandStatus(str, Enum):
    PENDING = "pending"
    RECEIVED = "received"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILURE = "failure"
    INVALIDATED = "invalidated"

    @staticmethod
    def from_str(label):
        if label == 'pending':
            return CommandStatus.PENDING
        elif label == 'received':
            return CommandStatus.RECEIVED
        elif label == 'processing':
            return CommandStatus.PROCESSING
        elif label == 'success':
            return CommandStatus.SUCCESS
        elif label == 'failure':
            return CommandStatus.FAILURE
        elif label == 'invalidated':
            return CommandStatus.INVALIDATED
        else:
            raise NotImplementedError


class CommandDetails:
    def __init__(self, commandMsg: dict | None = None):
        if commandMsg is not None:
            self.command = commandMsg["command"]
            self.id = uuid.UUID(commandMsg["commandId"])
            self.type = commandMsg["datatype"]
            if self.type == "string":
                self.data = commandMsg["data"]
            elif self.type == "binary":
                base64_bytes = commandMsg["data"].encode("ascii")
                data_bytes = base64.b64decode(base64_bytes)
                self.data = data_bytes
            else:
                raise Exception("Invalid datatype")
            self.exp = datetime.datetime.fromtimestamp(commandMsg["exp"] / 1000)
            self.status = None
            self.updated = None
        else:
            self.command = None
            self.id = None
            self.type = None
            self.data = None
            self.exp = None
            self.status = None
            self.updated = None
            self.issued = None


class VSUpdate:
    def __init__(self, VSUpdateMessge: dict | None = None):
        if VSUpdateMessge is not None:
            self.namespace = VSUpdateMessge["namespace"]
            self.type = VSDataType.from_str(VSUpdateMessge["type"])
            self.key = VSUpdateMessge["key"]
            if self.type == VSDataType.STRING:
                self.value = VSUpdateMessge["value"]
            elif self.type == VSDataType.BINARY:
                base64_bytes = VSUpdateMessge["data"].encode("ascii")
                data_bytes = base64.b64decode(base64_bytes)
                self.data = data_bytes
            elif self.type == VSDataType.FLOAT:
                self.value = VSUpdateMessge["value"]
            elif self.type == VSDataType.BOOL:
                self.value = VSUpdateMessge["value"]
            self.value = VSUpdateMessge["value"]
            self.modified = datetime.datetime.fromtimestamp(VSUpdateMessge["modified"])
        else:
            self.namespace = None
            self.type = None
            self.key = None
            self.value = None
            self.modified = None


class VSDataType(str, Enum):
    BINARY = "binary"
    STRING = "string"
    FLOAT = "float"
    BOOL = "bool"

    @staticmethod
    def from_str(label):
        if label == 'binary':
            return VSDataType.BINARY
        elif label == 'string':
            return VSDataType.STRING
        elif label == 'float':
            return VSDataType.FLOAT
        elif label == 'bool':
            return VSDataType.BOOL
        else:
            return NotImplementedError


class AnedyaEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'toJSON'):
            return obj.toJSON()
        else:
            return json.JSONEncoder.default(self, obj)
