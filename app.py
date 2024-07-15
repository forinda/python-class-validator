from .src import NumberValidator, StringSanitizer, StringValidator, BooleanValidator


class FieldValidationError(Exception):
    pass


class Fields:
    @staticmethod
    def string():
        return StringValidator()

    @staticmethod
    def number():
        return NumberValidator()

    @staticmethod
    def boolean():
        return BooleanValidator()


class ValidatorMeta(type):
    def __new__(cls, name, bases, dct):
        dct['_fields'] = {k: v for k, v in dct.items() if isinstance(
            v, (StringValidator, NumberValidator))}
        return super().__new__(cls, name, bases, dct)

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
