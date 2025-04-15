import datetime

class ImageEmptyException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.timestamp = datetime.datetime.now()

class ColorRecognitionListErrorException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.timestamp = datetime.datetime.now()

class ColorAlreadyFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.timestamp = datetime.datetime.now()

class DebugParameterErrorException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.timestamp = datetime.datetime.now()