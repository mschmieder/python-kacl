class KACLValidationError():
    def __init__(self, line="", line_number=0, start_character_pos=None, end_character_pos=None, error_message=""):
        self.__line_number = line_number
        self.__start_character_pos = start_character_pos
        self.__end_character_pos = end_character_pos
        self.__error_message = error_message
        self.__line = line

    def line_number(self):
        return self.__line_number

    def position(self):
        return self.__start_character_pos, self.__end_character_pos

    def line(self):
        return self.__line

    def error_message(self):
        return self.__error_message


class KACLValidation():
    def __init__(self):
        self.__validation_errors = []

    def is_valid(self):
        return (len(self.__validation_errors) == 0)

    def errors(self):
        return self.__validation_errors

    def add_error(self, line, line_number, error_message, start_character_pos=None, end_character_pos=None):
        self.__validation_errors.append(KACLValidationError(line=line,
                                                            line_number=line_number,
                                                            start_character_pos=start_character_pos,
                                                            end_character_pos=end_character_pos,
                                                            error_message=error_message))


    def convert_to_dict(self):
        validation_map = dict()
        validation_map['valid'] = (len(self.__validation_errors) == 0)
        errors = []
        for error in self.__validation_errors:
            error_map = {
                "line": error.line(),
                "line_number": error.line_number(),
                "start_char_pos": error.position()[0],
                "end_character_pos": error.position()[1],
                "error_message": error.error_message()
            }
            errors.append(error_map)
        validation_map['errors'] = errors
        return validation_map
