class CoilNotFoundException(Exception):
    """Custom exception raised when a requested coil cannot be located.

    This exception is typically raised during database operations when:
    - Looking up a coil by ID that doesn't exist
    - Attempting to update a deleted/non-existent coil
    - Requesting statistics for a time range with no coils

    Attributes:
        message (str): Human-readable error description. Defaults to
            "Coil not found" if not provided explicitly.
    """
    def __init__(self, message: str = "Coil not found"):
        self.message = message
        super().__init__(self.message)
