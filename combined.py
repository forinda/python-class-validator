class BaseValidator(object):
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

    def add_validator(self, validator, message, **kwargs):
        """
        A method for adding a validator to the list.
        """
        self.validators.append((validator, message, kwargs))
        return self


class BooleanField(BaseValidator):

    def boolean(self, /, message="Must be a boolean", **kwargs):
        """
        Boolean values: This method is for checking for only boolean input
        and additional constraints like 'empty' and 'required'.
        """
        self.add_validator(self.__validate__, message, **kwargs)
        return self

    def __validate__(self, value, default=False):
        """
        Run the validator for boolean values with additional constraints.
        """
        if value is None and isinstance(default, bool):
            return False, default

        if not isinstance(value, bool):
            return True, None
        return False, value


class NumberField(BaseValidator):
    def __init__(self):
        self.validators = []

    def number(self, /, message="Must be a number", default=None, **kwargs):
        """
        Any numbers: This method is for checking for only floating point numbers or integers
        e.g ` a = 4 or b = 5.4`
        """
        self.add_validator(self.__validate__, message, **{
                           "default": default, ** kwargs})
        return self

    def __validate__(self, value, /, allow_empty=False, default=None, min=None, max=None):
        """Run the validator for number type `(float, int)`"""
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

    def string(self, /, message="Must be a string", default=None, min_length=None, max_length=None, allow_empty=False,**kwargs):
        kargs ={
            'min_length': min_length,
            'max_length': max_length,
            'allow_empty': allow_empty,
            "default": default
        }
        self.add_validator(self.__validate__, message, **kargs)
        return self

    def __validate__(self, value, /, min_length=None, max_length=None, allow_empty=False):
        """Run validation for string and its constraints"""
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
    string=StringField().string
    boolean=BooleanField().boolean
    number=NumberField().number

class ValidatorMeta(type):
    def __new__(cls, name, bases, dct):
        dct['_fields'] = {k: v for k, v in dct.items() if isinstance(
            v, (StringField, NumberField,BooleanField))}
        new_class= super().__new__(cls, name, bases, dct)
        for field_name,field in dct['_fields'].items():
            """Getter"""
            def getter(self,name=field_name): return self.__dict__.get(name)
            """Settter"""
            def setter(self,value,name=field_name,field=field):
                error,field_value = field.validate(value)
                if error:
                    raise FieldValidationError({name:error})
                self.__dict__[name]=field_value
                setattr(new_class,field_name,property(getter,setter))
        return new_class



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
    first_name= Field.string()
    last_name = Field.string()

p1 = PersonModel()
p1.first_name=False
print(p1.validate())
