import datetime

class VideoCaptureReadException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.timestamp = datetime.datetime.now()

class CameraTypeErrorException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.timestamp = datetime.datetime.now()

class CVFrameEmptyException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.timestamp = datetime.datetime.now()

class DecisionPointOutOfRangeException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.timestamp = datetime.datetime.now()