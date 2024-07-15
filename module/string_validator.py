class StringValidator:
    def __init__(self):
        self.validators = []

    def validate(self, value):
        """
        A method for processing all the methods under the string constructor
        """
        errors = set()
        for validator, message, kwargs in self.validators:
            error = validator(value, **kwargs)
            if error:
                errors.add(message)
        return list(errors)

    def string(self, message="Must be a string"):
        self.validators.append((self.__validate_string__, message))
        return self

    def __validate_string__(self, value):
        """Run validation for string"""
        if not isinstance(value, str):
            return True
        return False

    def min_length(self, message="Must be a string", **kwargs):
        self.validators.append((self.__validate_min_length__, message, kwargs))
        return self

    def __validate_min_length__(self, value, min_length=1):
        """Run validation for string"""
        if not isinstance(value, str) and len(value) < min_length:
            return True
        return False

    def max_length(self, message="Must be a string", **kwargs):
        self.validators.append((self.__validate_max_length__, message, kwargs))
        return self

    def __validate_max_length__(self, value, max_length=1):
        """Run validation for string"""
        if not isinstance(value, str) and len(value) > max_length:
            return True
        return False
