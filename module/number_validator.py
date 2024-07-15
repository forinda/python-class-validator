
class NumberValidator(object):
    def __init__(self):
        self.validators = []

    def validate(self, value):
        """
        A method for processing all the methods under the number constructor
        """
        errors = set()
        for validator, message,kwargs in self.validators:
            error = validator(value,**kwargs)
            if error:
                errors.add(message)
        return list(errors)

    def float(self, message="Must be a floating point number",**kwargs):
        """
        Floating point numbers: This method is for checking for only floating point numbers
        e.g ` a = 4.4 `
        """
        self.validators.append((self.__validate_float__, message,kwargs))
        return self

    def __validate_float__(self, value):
        """Run the validator for floats"""
        if not isinstance(value, float):
            return True
        return False

    def integer(self, message="Must be a integer number",**kwargs):
        """
        Integer numbers: This method is for checking for only integer numbers
        e.g ` a = 4`
        """
        self.validators.append((self.__validate_integer__, message,kwargs))
        return self

    def __validate_integer__(self, value):
        """Run the validator for integers"""
        if not isinstance(value, int):
            return True
        return False

    def number(self, message="Must be a  number",**kwargs):
        """
        Any numbers: This method is for checking for only floating point numbers or integers
        e.g ` a = 4 or b = 5.4`
        """
        self.validators.append((self.__validate_number__, message,kwargs))
        return self

    def __validate_number__(self, value):
        """Run the validator for number type(float,int)"""
        if not isinstance(value, (float, int)):
            return True
        return False

    def __validate_min__(self, value, min=1):
        """Run the validator for minimum value"""
        if not isinstance(value, (float, int)) and value < min:
            return True
        return False

    def __validate_max__(self, value, max=255):
        """Run the validator for maximum value"""
        if not isinstance(value, (float, int)) and value > max:
            return True
        return False
