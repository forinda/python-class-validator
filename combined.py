from typing import Union


class BaseValidator:
    def __init__(self):
        self.validators = []

    def valid(self, value):
        """
        A method for processing all the validators added to the instance.
        """
        errors = set()
        for validator, message, kwargs in self.validators:
            valid_field, field_value = validator(value, **kwargs)
            if not valid_field:
                errors.add(message)
        return list(errors), value

    def add_validator(self, validator, message, kwargs={}):
        """
        A method for adding a validator to the list.
        """
        self.validators.append((validator, message, kwargs))
        return self


class BaseModel:
    class BooleanField(BaseValidator):
        def boolean(self, /, message="Must be a boolean", default: bool = None):
            """
            Boolean values: This method is for checking for only boolean input
            and additional constraints like 'empty' and 'required'.
            """
            karg = {"default": default}
            self.add_validator(self.__is_valid__, message, karg)
            return self

        def __is_valid__(self, value, **kwargs):
            """
            Run the validator for boolean values with additional constraints.
            """
            default = kwargs.get('default', False)
            if default is not None and not isinstance(default, bool):
                return False, None
            if value is None and isinstance(default, bool):
                return True, default

            if not isinstance(value, bool):
                return False, None
            return True, value

    class NumberField(BaseValidator):
        def number(self, /, message="Must be a number", default: Union[float, int] = None, allow_empty: bool = False, min: Union[float, int] = None, max: Union[float, int] = None, choices: Union[list, tuple] = None):
            """
            This method is for validating numerical inputs and can include additional constraints such as minimum and maximum values, 
            allowing empty values, and default values.

            Args:
                `message (str, optional):` The error message to display if validation fails. Defaults to "Must be a number".
                `default (float|int, optional):` The default value to use if the input is None. Defaults to None.
                `min (float|int, optional):` The minimum value allowed. If the value is smaller, validation will fail. Defaults to None.
                `max (float|int, optional):` The maximum value allowed. If the value is larger, validation will fail. Defaults to None.
                `choices (list, optional):` A list of allowed values. If the value is not in the list, validation will fail. Defaults to None.
                `allow_empty (bool, optional):` If set to True, allows the value to be None. Defaults to False.

            Returns:
                `NumberField`: Returns the instance of the NumberField for method chaining.
            """
            kargs = {
                "default": default,
                "allow_empty": allow_empty,
                "min": min,
                "max": max,
                "choices": choices
            }
            self.add_validator(self.__is_valid__, message, kargs)
            return self

        def __is_valid__(self, value, /, **kwargs):
            """Run the validator for number type `(float, int)`"""
            allow_empty = kwargs.get('allow_empty', False)
            default = kwargs.get('default', None)
            min = kwargs.get('min', None)
            max = kwargs.get('max', None)
            choices = kwargs.get('choices', None)
            if allow_empty and value is None:
                return True, default
            if not isinstance(value, (float, int)):
                return False, None
            if min is not None and value < min:
                return False, None
            if max is not None and value > max:
                return False, None
            if isinstance(choices, (list, tuple)) and len(choices) > 0 and value not in choices:
                return False, None
            return True, value

    class StringField(BaseValidator):
        def string(self, /, message="Must be a string", default=None, min_length=None, max_length=None, allow_empty=False, choices=None):
            """
            This method is for validating string inputs and can include additional constraints such as minimum and maximum length, 
            allowing empty values, and default values.

            Args:
                `message (str, optional):` The error message to display if validation fails. Defaults to "Must be a string".
                `default (str, optional):` The default value to use if the input is None. Defaults to None.
                `min_length (int, optional):` The minimum length of the string. If the string is shorter, validation will fail. Defaults to None.
                `max_length (int, optional):` The maximum length of the string. If the string is longer, validation will fail. Defaults to None.
                `choices (list, optional):` A list of allowed values. If the value is not in the list, validation will fail. Defaults to None.
                `allow_empty (bool, optional):` If set to True, allows the value to be None. Defaults to False.
                `**kwargs:` Additional keyword arguments to pass to the validator.

            Returns:
                StringField: Returns the instance of the StringField for method chaining.
            """
            kargs = {
                'min_length': min_length,
                'max_length': max_length,
                'allow_empty': allow_empty,
                "default": default,
                'choices': choices
            }
            self.add_validator(self.__is_valid__, message, kargs)
            return self

        def __is_valid__(self, value, /, **kwargs):
            """Run validation for string and its constraints"""
            min_length = kwargs.get('min_length', None)
            max_length = kwargs.get('max_length', None)
            allow_empty = kwargs.get('allow_empty', False)
            default = kwargs.get('default', None)
            choices = kwargs.get('choices', None)
            if allow_empty and value is None:
                return True, default
            if default is not None and not isinstance(default, str):
                return False, None
            if not isinstance(value, str):
                return False, None
            if min_length is not None and len(value) < min_length:
                return False, None
            if max_length is not None and len(value) > max_length:
                return False, None
            if isinstance(choices, (tuple, list)) and len(choices) > 0 and value not in choices:
                return False, None
            return True, value


class ValidationError(Exception):
    """Base class for validation errors."""
    pass


class FieldValidationError(Exception):
    """Exception raised for errors in the field validation process.

    Attributes:
        field -- field in which the error occurred
        errors -- explanation of the errors
    """

    def __init__(self, message: str, errors: dict):
        super().__init__(message)
        self.errors = errors


class Field:
    string = BaseModel.StringField().string
    boolean = BaseModel.BooleanField().boolean
    number = BaseModel.NumberField().number


class ValidatorMeta(type):
    def __new__(cls, name, bases, dct):
        dct['_fields'] = {k: v for k,
                          v in dct.items() if isinstance(v, BaseValidator)}
        new_class = super().__new__(cls, name, bases, dct)
        for field_name, field in dct['_fields'].items():
            """Getter"""

            def getter(self, name=field_name):
                return self.__dict__.get(name)

            """Setter"""

            def setter(self, value, name=field_name, field=field):
                # errors, field_value = field.valid(value)
                # if errors:
                #     raise FieldValidationError('Field validation failed',errors)
                self.__dict__[name] = value

            setattr(new_class, field_name, property(getter, setter))
        return new_class


class ValidationModel(metaclass=ValidatorMeta):
    def __init__(self, **kwargs):
        for field_name, val in kwargs.items():
            if field_name in self._fields:
                setattr(self, field_name, val)

    def validate(self):
        errors = {}
        for field_name, field_validator in self._fields.items():
            value = getattr(self, field_name, None)
            field_errors, _ = field_validator.valid(value)
            if field_errors:
                errors[field_name] = field_errors
        if errors:
            raise FieldValidationError(f'{field_name}: Field validation failed', errors)

    def build(self):

        return {k: getattr(self, k) for k in self._fields.keys() if not callable(getattr(self, k))}
        # return my_obj


if __name__ == '__main__':
    class PersonModel(ValidationModel):
        is_admin = Field.boolean(default=True)
        gpa = Field.number(default=4.5)
        last_name = Field.string(max_length=5)

    p1 = PersonModel(is_admin=False, gpa=4.5,
                     last_name="Smiths", first_name="Mike")
    # try:
    p1.validate()
    final_obj = p1.build()
    print(final_obj)
    # except FieldValidationError as e:
    #     print(f"Error: {e.errors}")
