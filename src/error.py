class FieldValidationError(Exception):
    """Exception raised for errors in the field validation process.

    Attributes:
        field -- field in which the error occurred
        errors -- explanation of the errors
    """

    def __init__(self, message: str, errors: dict):
        super().__init__(message)
        self.errors = errors
