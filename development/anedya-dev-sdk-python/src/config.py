# src/config.py

class AnedyaConfig:
    def __init__(self, api_token, device_id=None, mode='HTTP'):
        self.api_token = api_token
        self.device_id = device_id
        self.mode = mode

    @classmethod
    def from_device_id(cls, api_token, device_id, mode='HTTP'):
        # Initialize the configuration with device ID
        return cls(api_token, device_id, mode)

    @classmethod
    def from_tls_certificate(cls, api_token, tls_certificate_path, mode='MQTT'):
        # Initialize the configuration with TLS certificate
        # Additional logic to load TLS certificate goes here
        return cls(api_token, device_id=None, mode)

    def to_dict(self):
        return {
            'api_token': self.api_token,
            'device_id': self.device_id,
            'mode': self.mode
        }
