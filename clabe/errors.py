from pydantic.errors import PydanticValueError


class BankCodeValidationError(PydanticValueError):
    code = 'clabe.bank_code'
    msg_template = 'código de banco no es válido'


class ClabeControlDigitValidationError(PydanticValueError):
    code = 'clabe.control_digit'
    msg_template = 'clabe dígito de control no es válido'


class BankCodeAlreadyExistsError(PydanticValueError):
    code = 'clabe.bank_code_already_exists'
    msg_template = 'código de banco ya existe'


class BankNameAlreadyExistsError(PydanticValueError):
    code = 'clabe.bank_name_already_exists'
    msg_template = 'nombre de banco ya existe'
