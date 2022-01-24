class PreconditionFailedException(Exception):

    def __init__(self, message=""):
        self.message = "412: Precondition Failed: " + message
        super().__init__(self.message)
