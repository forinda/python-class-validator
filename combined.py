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
        return list(errors), field_value

    def add_validator(self, validator, message, kwargs={}):
        """
        A method for adding a validator to the list.
        """
        self.validators.append((validator, message, kwargs))
        # return self


class BooleanField(BaseValidator):

    def boolean(self, /, message="Must be a boolean", **kwargs):
        """
        Boolean values: This method is for checking for only boolean input
        and additional constraints like 'empty' and 'required'.
        """
        self.add_validator(self.__is_valid__, message, kwargs)
        return self

    def __is_valid__(self, value, **kwargs):
        """
        Run the validator for boolean values with additional constraints.
        """
        default = kwargs.get('default', False)
        if value is None and isinstance(default, bool):
            return True, default

        if not isinstance(value, bool):
            return False, None
        return True, value


class NumberField(BaseValidator):
    def __init__(self):
        self.validators = []

    def number(self, /, message="Must be a number", default=None, **kwargs):
        """
        This method is for validating numerical inputs and can include additional constraints such as minimum and maximum values, 
        allowing empty values, and default values.

        Args:
            `message (str, optional):` The error message to display if validation fails. Defaults to "Must be a number".
            `default (float|int, optional):` The default value to use if the input is None. Defaults to None.
            `min (float|int, optional):` The minimum value allowed. If the value is smaller, validation will fail. Defaults to None.
            `max (float|int, optional):` The maximum value allowed. If the value is larger, validation will fail. Defaults to None.
            `allow_empty (bool, optional):` If set to True, allows the value to be None. Defaults to False.
            `**kwargs:` Additional keyword arguments to pass to the validator.

        Returns:
            `NumberField`: Returns the instance of the NumberField for method chaining.
        """
        self.add_validator(self.__is_valid__, message, **{
                           "default": default, ** kwargs})
        # return self

    def __is_valid__(self, value, /,**kwargs):
        """Run the validator for number type `(float, int)`"""
        allow_empty = kwargs.get('allow_empty', False)
        default = kwargs.get('default', None)
        min = kwargs.get('min', None)
        max = kwargs.get('max', None)
        if allow_empty and value is None:
            return False, default
        if not isinstance(value, (float, int)):
            return True, value
        if min is not None and value < min:
            return True, value
        if max is not None and value > max:
            return True, value
        return False, value


class StringField(BaseValidator):
    def __init__(self):
        self.validators = []

    def string(self, /, message="Must be a string", default=None, min_length=None, max_length=None, allow_empty=False):
        """
        This method is for validating string inputs and can include additional constraints such as minimum and maximum length, 
        allowing empty values, and default values.

        Args:
            `message (str, optional):` The error message to display if validation fails. Defaults to "Must be a string".
            `default (str, optional):` The default value to use if the input is None. Defaults to None.
            `min_length (int, optional):` The minimum length of the string. If the string is shorter, validation will fail. Defaults to None.
            `max_length (int, optional):` The maximum length of the string. If the string is longer, validation will fail. Defaults to None.
            `allow_empty (bool, optional):` If set to True, allows the value to be None. Defaults to False.
            `**kwargs:` Additional keyword arguments to pass to the validator.

        Returns:
            StringField: Returns the instance of the StringField for method chaining.
        """
        kargs = {
            'min_length': min_length,
            'max_length': max_length,
            'allow_empty': allow_empty,
            "default": default
        }
        self.add_validator(self.__is_valid__, message, kargs)
        # return self

    def __is_valid__(self, value, /, **kwargs):
        """Run validation for string and its constraints"""
        min_length = kwargs.get('min_length', None)
        max_length = kwargs.get('max_length', None)
        allow_empty = kwargs.get('allow_empty', False)
        if allow_empty and value is None:
            return False, value
        if not isinstance(value, str):
            return True, value
        if min_length is not None and len(value) < min_length:
            return True, value
        if max_length is not None and len(value) > max_length:
            return True, value
        return False, value


class FieldValidationError(Exception):
    pass


class Field:
    string = StringField().string
    boolean = BooleanField().boolean
    number = NumberField().number


class ValidatorMeta(type):
    def __new__(cls, name, bases, dct):
        dct['_fields'] = {k: v for k, v in dct.items() if isinstance(
            v, (StringField, NumberField, BooleanField))}
        new_class = super().__new__(cls, name, bases, dct)
        for field_name, field in dct['_fields'].items():
            """Getter"""

            def getter(self, name=field_name): return self.__dict__.get(name)
            """Settter"""

            def setter(self, value, name=field_name, field=field):
                error, field_value = field.validate(value)
                if error:
                    raise FieldValidationError({name: error})
                self.__dict__[name] = field_value
                setattr(new_class, field_name, property(getter, setter))
        return new_class


class ValidationModel(metaclass=ValidatorMeta):
    def __init__(self, **kwargs) -> None:
        for field_name, val in kwargs.items():
            if field_name in self._fields:
                setattr(self, field_name, val)

    def validate(self):

        errors = {}
        for field_name, field_validator in self._fields.items():
            value = getattr(self, field_name, None)
            field_errors,_ = field_validator.valid(value)
            # print(
            #     f"Field name: {field_name},value: {value}, errors: {field_errors} ")
            # print
            if field_errors and len(field_errors) > 0:
                errors[field_name] = field_errors
        if errors:
            # print(errors)
            raise FieldValidationError(errors)


class PersonModel(ValidationModel):
    is_admin = BooleanField().boolean(default="True")
    is_late = BooleanField().boolean(default="True")
    # last_name = Field.string()


p1 = PersonModel(is_late=False)
# p1.is_admin = True
print(p1.validate())