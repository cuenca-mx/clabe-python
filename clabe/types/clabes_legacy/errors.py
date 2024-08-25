from pydantic.errors import PydanticValueError


class BankCodeValidationError(PydanticValueError):
    code = 'clabe.bank_code'
    msg_template = 'código de banco no es válido'


class ClabeControlDigitValidationError(PydanticValueError):
    code = 'clabe.control_digit'
    msg_template = 'clabe dígito de control no es válido'
