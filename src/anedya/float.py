

class FloatData:
    def __init__(self, name :str, timestamp :int, value: float):
        self.variable = name
        self.timestamp = timestamp
        self.value = value
    def toJSON(self):
        dict = {
            "variable":self.variable,
            "timestamp":self.timestamp,
            "value": self.value
        }
        return dict