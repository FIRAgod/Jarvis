import datetime

class ImageEmptyException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.timestamp = datetime.datetime.now()

class CVFrameEmptyException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.timestamp = datetime.datetime.now()

class DebugParameterErrorException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.timestamp = datetime.datetime.now()

class DecisionPointOutOfRangeException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.timestamp = datetime.datetime.now()