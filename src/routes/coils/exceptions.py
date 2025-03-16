class CoilNotFoundException(Exception):
    def __init__(self, message: str = "Coil not found"):
        self.message = message
        super().__init__(self.message)
