

class FloatData:
    def __init__(self, variable :str, timestamp_milli :int, value: float):
        self.variable = variable
        self.timestamp = timestamp_milli
        self.value = value
    def toJSON(self):
        dict = {
            "variable":self.variable,
            "timestamp":self.timestamp,
            "value": self.value
        }
        return dict