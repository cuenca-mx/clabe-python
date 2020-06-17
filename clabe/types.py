from typing import TYPE_CHECKING, ClassVar

from pydantic.errors import NotDigitError
from pydantic.validators import (
    constr_length_validator,
    constr_strip_whitespace,
    str_validator,
)

from .errors import BankCodeValidationError, ClabeControlDigitValidationError
from .validations import BANK_NAMES, BANKS, compute_control_digit

if TYPE_CHECKING:
    from pydantic.typing import CallableGenerator


def validate_digits(v: str) -> str:
    if not v.isdigit():
        raise NotDigitError
    return v


class Clabe(str):
    """
    Based on: https://es.wikipedia.org/wiki/CLABE
    """

    strip_whitespace: ClassVar[bool] = True
    min_length: ClassVar[int] = 18
    max_length: ClassVar[int] = 18

    def __init__(self, clabe: str):
        self.bank_code_abm = clabe[:3]
        self.bank_code_banxico = BANKS[clabe[:3]]
        self.bank_name = BANK_NAMES[self.bank_code_banxico]

    @classmethod
    def __get_validators__(cls) -> 'CallableGenerator':
        yield str_validator
        yield constr_strip_whitespace
        yield constr_length_validator
        yield validate_digits
        yield cls.validate_bank_code_abm
        yield cls.validate_control_digit
        yield cls

    @classmethod
    def validate_bank_code_abm(cls, clabe: str) -> str:
        if clabe[:3] not in BANKS.keys():
            raise BankCodeValidationError
        return clabe

    @classmethod
    def validate_control_digit(cls, clabe: str) -> str:
        if clabe[-1] != compute_control_digit(clabe):
            raise ClabeControlDigitValidationError
        return clabe

    @property
    def bank_code(self):
        return self.bank_code_banxico
