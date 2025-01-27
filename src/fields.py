from typing import Union
from datetime import datetime, date
from . import BaseValidator


# from field_validator import BaseValidator

class BooleanField(BaseValidator):
    def boolean(self, /,
                message="Must be a boolean",
                default: bool = None,
                empty_message="Value cannot be empty"):
        """
        Boolean values: This method is for checking for only boolean input
        and additional constraints like 'empty' and 'required'.

        Args:
            `message (str, optional):` The error message to display if validation fails. Defaults to "Must be a boolean".
            `default (bool, optional):` The default value to use if the input is None. Defaults to None.
            `empty_message (str, optional):` The error message if the value is empty but required. Defaults to "Value cannot be empty".

        Returns:
            BooleanField: Returns the instance of the BooleanField for method chaining.
        """
        karg = {
            "default": default,
            "messages": {
                "type": message,
                "empty": empty_message
            }
        }
        self.add_validator(self.__is_valid__, karg['messages'], karg)
        return self

    def __is_valid__(self, value, **kwargs):
        """
        Run the validator for boolean values with additional constraints.
        """
        default = kwargs.get('default', None)
        messages = kwargs.get('messages', {})

        if value is None and default is not None:
            return True, default, None
        if not isinstance(value, bool):
            return False, None, messages.get("type")
        return True, value, None


class NumberField(BaseValidator):
    def number(self, /,
               message="Must be a number",
               default: Union[float, int, None] = None,
               allow_empty: bool = False,
               min_value: Union[float, int, None] = None,
               max_value: Union[float, int, None] = None,
               choices: Union[list, tuple, None] = None,
               min_value_message="Value must be at least {min_value}",
               max_value_message="Value must be at most {max_value}",
               choices_message="Value is not allowed",
               empty_message="Value cannot be empty"):
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
            `min_value_message (str, optional):` The error message if the value is smaller than min_value. Defaults to "Value must be at least {min_value}".
            `max_value_message (str, optional):` The error message if the value is larger than max_value. Defaults to "Value must be at most {max_value}".
            `choices_message (str, optional):` The error message if the value is not in the choices list. Defaults to "Value is not allowed".
            `empty_message (str, optional):` The error message if the value is empty but allow_empty is False. Defaults to "Value cannot be empty".

        Returns:
            `NumberField`: Returns the instance of the NumberField for method chaining.
        """
        k_args = {
            "default": default,
            "allow_empty": allow_empty,
            "min_value": min_value,
            "max_value": max_value,
            "choices": choices,
            "messages": {
                "type": message,
                "min_value": min_value_message,
                "max_value": max_value_message,
                "choices": choices_message,
                "empty": empty_message
            }
        }
        self.add_validator(self.__is_valid__, k_args["messages"], k_args)
        return self

    def __is_valid__(self, value, /, **kwargs):
        """Run the validator for number type `(float, int)`"""
        allow_empty = kwargs.get('allow_empty', False)
        default = kwargs.get('default', None)
        min_val = kwargs.get('min_value', None)
        max_val = kwargs.get('max_value', None)
        choices = kwargs.get('choices', None)
        messages = kwargs.get('messages', {})

        if allow_empty and value is None:
            return True, default, None
        if not isinstance(value, (float, int)):
            return False, None, messages.get("type")
        if isinstance(min_val, (float, int)) and min_val is not None and value < min_val:
            return False, None, messages.get("min_value").format(min_value=min_val)
        if isinstance(max_val, (float, int)) and max_val is not None and value > max_val:
            return False, None, messages.get("max_value").format(max_value=max_val)
        if isinstance(choices, (list, tuple)) and len(choices) > 0 and value not in choices:
            return False, None, messages.get("choices")
        return True, value, None


class StringField(BaseValidator):
    def string(self, /,
               message="Must be a string",
               default: Union[str, None] = None,
               min_length: Union[int, float, None] = None,
               max_length: Union[int, float, None] = None,
               allow_empty: bool = False,
               choices: Union[list, tuple, None] = None,
               min_length_message="String must be at least {min_length} characters long",
               max_length_message="String must be at most {max_length} characters long",
               choices_message="String is not an allowed value",
               empty_message="String cannot be empty"):
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
            `min_length_message (str, optional):` The error message if the string is shorter than min_length. Defaults to "String must be at least {min_length} characters long".
            `max_length_message (str, optional):` The error message if the string is longer than max_length. Defaults to "String must be at most {max_length} characters long".
            `choices_message (str, optional):` The error message if the string is not in the choices list. Defaults to "String is not an allowed value".
            `empty_message (str, optional):` The error message if the string is empty but allow_empty is False. Defaults to "String cannot be empty".

        Returns:
            StringField: Returns the instance of the StringField for method chaining.
        """
        kargs = {
            'min_length': min_length,
            'max_length': max_length,
            'allow_empty': allow_empty,
            'default': default,
            'choices': choices,
            'messages': {
                'type': message,
                'min_length': min_length_message,
                'max_length': max_length_message,
                'choices': choices_message,
                'empty': empty_message
            }
        }
        self.add_validator(self.__is_valid__, kargs['messages'], kargs)
        return self

    def __is_valid__(self, value, /, **kwargs):
        """Run validation for string and its constraints"""
        min_length = kwargs.get('min_length', None)
        max_length = kwargs.get('max_length', None)
        allow_empty = kwargs.get('allow_empty', False)
        default = kwargs.get('default', None)
        choices = kwargs.get('choices', None)
        messages = kwargs.get('messages', {})

        if allow_empty and value is None:
            return True, default, None
        if not isinstance(value, str):
            return False, None, messages.get('type')
        if isinstance(min_length, (int, float)) and min_length is not None and len(value) < min_length:
            return False, None, messages.get('min_length').format(min_length=min_length)
        if isinstance(max_length, (int, float)) and max_length is not None and len(value) > max_length:
            return False, None, messages.get('max_length').format(max_length=max_length)
        if isinstance(choices, (list, tuple)) and len(choices) > 0 and value not in choices:
            return False, None, messages.get('choices')
        return True, value, None


class DateField(BaseValidator):
    def date(
        self,
        message="Must be a valid date",
        default: Union[datetime, date, None] = None,
        allow_empty: bool = False,
        min_date: Union[datetime, date, None] = None,
        max_date: Union[datetime, date, None] = None,
        min_date_message="Date must be on or after {min_date}",
        max_date_message="Date must be on or before {max_date}",
        empty_message="Date cannot be empty"
    ):
        """
        This method is for validating date inputs and can include additional constraints such as minimum and maximum dates,
        allowing empty values, and default values.

        Args:
            `message (str, optional):` The error message to display if validation fails. Defaults to "Must be a valid date".
            `default (datetime|date, optional):` The default value to use if the input is None. Defaults to current date and time.
            `min_date (datetime|date, optional):` The minimum date allowed. If the value is earlier, validation will fail. Defaults to None.
            `max_date (datetime|date, optional):` The maximum date allowed. If the value is later, validation will fail. Defaults to None.
            `allow_empty (bool, optional):` If set to True, allows the value to be None. Defaults to False.
            `min_date_message (str, optional):` The error message if the date is earlier than min_date. Defaults to "Date must be on or after {min_date}".
            `max_date_message (str, optional):` The error message if the date is later than max_date. Defaults to "Date must be on or before {max_date}".
            `empty_message (str, optional):` The error message if the date is empty but required. Defaults to "Date cannot be empty".

        Returns:
            `DateField`: Returns the instance of the DateField for method chaining.
        """
        if default is None:
            default = datetime.now()

        k_args = {
            "default": default,
            "allow_empty": allow_empty,
            "min_date": min_date,
            "max_date": max_date,
            "messages": {
                "type": message,
                "min_date": min_date_message,
                "max_date": max_date_message,
                "empty": empty_message
            }
        }
        self.add_validator(self.__is_valid__, k_args["messages"], k_args)
        return self

    def __is_valid__(
        self,
        value: Union[datetime, date, None],
        /,
        **kwargs
    ) -> tuple:
        """Run the validator for date type `(datetime, date)`"""
        allow_empty = kwargs.get('allow_empty', False)
        default = kwargs.get('default', None)
        min_date = kwargs.get('min_date', None)
        max_date = kwargs.get('max_date', None)
        messages = kwargs.get('messages', {})

        if allow_empty and value is None:
            return True, default, None

        if not isinstance(value, (datetime, date)):
            return False, None, messages.get("type")

        if min_date is not None and value < min_date:
            return False, None, messages.get("min_date", "").format(min_date=min_date)

        if max_date is not None and value > max_date:
            return False, None, messages.get("max_date", "").format(max_date=max_date)

        return True, value, None


class FieldMixin:
    """Abstract field consolidator class for available fields for validation"""
    @staticmethod
    def string(message="Must be a string",
               default: Union[str, None] = None,
               min_length: Union[int, float, None] = None,
               max_length: Union[int, float, None] = None,
               allow_empty: bool = False,
               choices: Union[list, tuple, None] = None,
               min_length_message="String must be at least {min_length} characters long",
               max_length_message="String must be at most {max_length} characters long",
               choices_message="String is not an allowed value",
               empty_message="String cannot be empty"):
        return StringField().string(message, default=default, min_length=min_length, max_length=max_length, allow_empty=allow_empty, choices=choices, min_length_message=min_length_message, max_length_message=max_length_message, choices_message=choices_message, empty_message=empty_message)

    @staticmethod
    def boolean(message="Must be a boolean",
                default: bool = None,
                empty_message="Value cannot be empty"):
        return BooleanField().boolean(message, default=default, empty_message=empty_message)

    @staticmethod
    def number(message="Must be a number",
               default: Union[float, int, None] = None,
               allow_empty: bool = False,
               min_value: Union[float, int, None] = None,
               max_value: Union[float, int, None] = None,
               choices: Union[list, tuple, None] = None,
               min_value_message="Value must be at least {min_value}",
               max_value_message="Value must be at most {max_value}",
               choices_message="Value is not allowed",
               empty_message="Value cannot be empty"):
        return NumberField().number(message=message, default=default, allow_empty=allow_empty, min_value=min_value, max_value=max_value, choices=choices, min_value_message=min_value_message, max_value_message=max_value_message, empty_message=empty_message, choices_message=choices_message)

    @staticmethod
    def date(message="Must be a valid date",
             default: Union[datetime, date, None] = None,
             allow_empty: bool = False,
             min_date: Union[datetime, date, None] = None,
             max_date: Union[datetime, date, None] = None,
             min_date_message="Date must be on or after {min_date}",
             max_date_message="Date must be on or before {max_date}",
             empty_message="Date cannot be empty"):
        return DateField().date(message, default=default, allow_empty=allow_empty, min_date=min_date, max_date=max_date, min_date_message=min_date_message, empty_message=empty_message, max_date_message=max_date_message,)
