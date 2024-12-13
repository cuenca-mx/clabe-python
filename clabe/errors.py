from pydantic.errors import PydanticValueError


class BankCodeValidationError(PydanticValueError):
    code = 'clabe.bank_code'
    msg_template = 'código de banco no es válido'


class ClabeControlDigitValidationError(PydanticValueError):
    code = 'clabe.control_digit'
    msg_template = 'clabe dígito de control no es válido'


class BankCodeABMAlreadyExistsError(PydanticValueError):
    code = 'clabe.bank_code_abm_already_exists'
    msg_template = 'código de banco ABM ya existe'


class BankCodeBanxicoAlreadyExistsError(PydanticValueError):
    code = 'clabe.bank_code_banxico_already_exists'
    msg_template = 'código de banco banxico ya existe'
