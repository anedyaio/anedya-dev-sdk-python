import json
from .encoder import AnedyaEncoder

class batch:
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