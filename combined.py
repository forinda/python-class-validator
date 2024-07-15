class BooleanValidator:
    def __init__(self):
        self.validators = []

    def validate(self, value):
        """
        A method for processing all the validators added to the instance.
        """
        errors = set()
        for validator, message, kwargs in self.validators:
            error = validator(value, **kwargs)
            if error:
                errors.add(message)
        return list(errors)

    def boolean(self, /, message="Must be a boolean", **kwargs):
        """
        Boolean values: This method is for checking for only boolean input
        and additional constraints like 'empty' and 'required'.
        """
        self.validators.append((self.__validate_boolean__, message, kwargs))
        return self

    def __validate_boolean__(self, value, default=False):
        """
        Run the validator for boolean values with additional constraints.
        """
        if value is None and isinstance(default, bool):
            return False, default

        if not isinstance(value, bool):
            return True, None
        return False, value


class NumberValidator:
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

    def number(self, message="Must be a number", **kwargs):
        """
        Any numbers: This method is for checking for only floating point numbers or integers
        e.g ` a = 4 or b = 5.4`
        """
        self.validators.append((self.__validate_number__, message, kwargs))
        return self

    def __validate_number__(self, value, allow_empty=False, min=None, max=None):
        """Run the validator for number type `(float, int)`"""
        if allow_empty and value is None:
            return False
        if not isinstance(value, (float, int)):
            return True
        if min is not None and value < min:
            return True
        if max is not None and value > max:
            return True
        return False


class StringValidator:
    def __init__(self):
        self.validators = []

    def validate(self, value):
        """
        A method for processing all the validators added to the instance.
        """
        errors = set()
        for validator, message, kwargs in self.validators:
            error = validator(value, **kwargs)
            if error:
                errors.add(message)
        return list(errors)

    def string(self, message="Must be a string", min_length=None, max_length=None, allow_empty=False):
        self.validators.append((self.__validate_string__, message, {
            'min_length': min_length,
            'max_length': max_length,
            'allow_empty': allow_empty
        }))
        return self

    def __validate_string__(self, value, min_length=None, max_length=None, allow_empty=False):
        """Run validation for string and its constraints"""
        if allow_empty and value is None:
            return False
        if not isinstance(value, str):
            return True
        if min_length is not None and len(value) < min_length:
            return True
        if max_length is not None and len(value) > max_length:
            return True
        return False


class FieldValidationError(Exception):
    pass


class ValidatorMeta(type):
    def __new__(cls, name, bases, dct):
        dct['_fields'] = {k: v for k, v in dct.items() if isinstance(
            v, (StringValidator, NumberValidator))}
        return super().__new__(cls, name, bases, dct)


class Fields:
    @staticmethod
    def string():
        return StringValidator().string

    @staticmethod
    def number():
        return NumberValidator().number

    @staticmethod
    def boolean():
        return BooleanValidator().boolean


class ValidationModel(metaclass=ValidatorMeta):
    def validate(self):
        errors = {}
        for field_name, field_validator in self._fields.items():
            value = getattr(self, field_name, None)
            field_errors = field_validator.validate(value)
            if field_errors:
                errors[field_name] = field_errors
        if errors:
            raise FieldValidationError(errors)


class PersonModel(ValidationModel):
    first_name: Fields.string
