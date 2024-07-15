from typing import Union

from . import BaseValidator


# from field_validator import BaseValidator


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
    def number(self, /, message="Must be a number", default: Union[float, int, None] = None, allow_empty: bool = False,
               min_value: Union[float, int, None] = None, max_value: Union[float, int, None] = None, choices: Union[list, tuple, None] = None):
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
            "min_value": min_value,
            "max_value": max_value,
            "choices": choices
        }
        self.add_validator(self.__is_valid__, message, kargs)
        return self

    def __is_valid__(self, value, /, **kwargs):
        """Run the validator for number type `(float, int)`"""
        allow_empty = kwargs.get('allow_empty', False)
        default = kwargs.get('default', None)
        min_val = kwargs.get('min_value', None)
        max_val = kwargs.get('max_value', None)
        choices = kwargs.get('choices', None)
        if allow_empty and value is None:
            return True, default
        if not isinstance(value, (float, int)):
            return False, None
        if isinstance(min_val, (float, int)) and min_val is not None and value < min_val:
            return False, None
        if isinstance(max_val, (float, int)) and max_val is not None and value > max_val:
            return False, None
        if isinstance(choices, (list, tuple)) and len(choices) > 0 and value not in choices:
            return False, None
        return True, value


class StringField(BaseValidator):
    def string(self, /, message="Must be a string", default: Union[str, None] = None, min_length: Union[int, float, None] = None, max_length: Union[int, float, None] = None, allow_empty=False,
               choices=None):
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
        if isinstance(min_length, int) and min_length is not None and len(value) < min_length:
            return False, None
        if isinstance(max_length, int) and max_length is not None and len(value) > max_length:
            return False, None
        if isinstance(choices, (tuple, list)) and len(choices) > 0 and value not in choices:
            return False, None
        return True, value


class Field:
    string = StringField().string
    boolean = BooleanField().boolean
    number = NumberField().number
