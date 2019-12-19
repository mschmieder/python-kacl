class KACLValidationError():
    def __init__(self, text, line_number, error_message):
        self.__line_number = line_number
        self.__error_message = error_message
        self.__text = text

    def line_number(self):
        return self.__line_number

    def text(self):
        return self.__text

    def error_message(self):
        return self.__error_message


class KACLValidation():
    def __init__(self):
        self.__validation_errors = []

    def is_valid(self):
        return (len(self.__validation_errors) == 0)

    def validation_errors(self):
        return self.__validation_errors

    def add_error(self, text, line_number, error_message):
        self.__validation_errors.append(KACLValidationError(text, line_number, error_message))