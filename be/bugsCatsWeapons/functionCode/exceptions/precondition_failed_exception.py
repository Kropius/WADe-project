class PreconditionFailedException(Exception):
    def __init__(self, message=""):
        self.message = "Precondition Failed: " + message
        super().__init__(self.message)
