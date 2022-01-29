class ResourceNotFoundException(Exception):
    def __init__(self, message=""):
        self.message = "Resource Not Found: " + message
        super().__init__(self.message)
