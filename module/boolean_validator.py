class BooleanValidator:
    def __init__(self):
        self.validators = []

    def validate(self, value):
        """
        A method for processing all the methods under the number constructor
        """
        errors = set()
        for validator, message, kwargs in self.validators:
            error = validator(value, **kwargs)
            if error:
                errors.add(message)
        return list(errors)

    def boolean(self, message="Must be a  number", **kwargs):
        """
        Boolean values: This method is for checking for only boolean input
        """
        self.validators.append((self.__validate_boolean__, message, kwargs))
        return self

    def __validate_boolean__(self, value):
        """Run the validator for floats"""
        if not isinstance(value, bool):
            return True
        return False
