import json
import time


class FloatData:
    def __init__(self, variable: str, value: float, timestamp_milli: int = int(time.time_ns() / 1000000)):
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


class AnedyaEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'toJSON'):
            return obj.toJSON()
        else:
            return json.JSONEncoder.default(self, obj)
