import pytest

from clabe.utils import pydantic_v1

if pydantic_v1():
    from pydantic.errors import NotDigitError
    from clabe.types.clabes_legacy.errors import (
        BankCodeValidationError,
        ClabeControlDigitValidationError,
    )
    from clabe.types import validate_digits

from clabe import BANK_NAMES, BANKS, compute_control_digit
from clabe.types import Clabe

VALID_CLABE = '646180157042875763'


# class Cuenta(BaseModel):
#     clabe: Clabe


@pytest.mark.skip
def test_valid_clabe():
    cuenta = Cuenta(clabe=VALID_CLABE)
    assert cuenta.clabe.bank_code_abm == '646'
    assert cuenta.clabe.bank_code_banxico == BANKS['646']
    assert cuenta.clabe.bank_name == BANK_NAMES[BANKS['646']]
    assert cuenta.clabe.bank_code == cuenta.clabe.bank_code_banxico


@pytest.mark.skipif(not pydantic_v1(), reason='Requires pydantic v1.x.x')
def test_clabe_digits():
    assert validate_digits(VALID_CLABE)


@pytest.mark.skipif(not pydantic_v1(), reason='Requires pydantic v1.x.x')
def test_clabe_not_digit():
    with pytest.raises(NotDigitError):
        validate_digits('h' * 18)


@pytest.mark.skipif(not pydantic_v1(), reason='Requires pydantic v1.x.x')
def test_invalid_bank_code_abm():
    clabe = '9' * 17
    clabe += compute_control_digit(clabe)
    with pytest.raises(BankCodeValidationError):
        Clabe.validate_bank_code_abm(clabe)


@pytest.mark.skipif(not pydantic_v1(), reason='Requires pydantic v1.x.x')
def test_invalid_control_digit():
    clabe = '001' + '9' * 15
    with pytest.raises(ClabeControlDigitValidationError):
        Clabe.validate_control_digit(clabe)
