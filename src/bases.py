from src import FieldValidationError


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


class Model(metaclass=ValidatorMeta):
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
            for key in errors.keys():
                raise FieldValidationError(f'{key}: Field validation failed', errors)
        return self

    def build(self):
        """
        Convert the model's fields to a JSON-serializable dictionary,
        excluding fields that are functions.
        """
        return {k: getattr(self, k) for k in self._fields.keys() if not callable(getattr(self, k))}
        # return my_obj