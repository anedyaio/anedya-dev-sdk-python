import json


class DataPoints:
    def __init__(self):
        self.data = []

    def append(self, datapoint):
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


class SubmitDataMQTTReq:
    def __init__(self, reqID: str, data: DataPoints):
        self.data = data
        self.reqID = reqID

    def toJSON(self):
        dict = {
            "reqId": self.reqID,
            "data": self.data.data
        }
        return dict

    def encodeJSON(self):
        data = json.dumps(self, cls=AnedyaEncoder)
        return data


class AnedyaEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'toJSON'):
            return obj.toJSON()
        else:
            return json.JSONEncoder.default(self, obj)


class FloatData:
    def __init__(self, variable: str, timestamp_milli: int, value: float):
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
