
class AnedyaInvalidConfig(Exception):
    """
    Exception for invalid Anedya Client Configuration
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class AnedyaInvalidProtocol(Exception):
    """
    This exception is raised when a particular action can not be carried out
    through certain protocol
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class AnedyaInvalidCredentials(Exception):
    """
    Raised when credentials are invalid
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class AnedyaRateLimitExceeded(Exception):
    """
    Raised when rate limit is exceeded
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class AnedyaException(Exception):
    """
    Raised when an exception occurs
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
