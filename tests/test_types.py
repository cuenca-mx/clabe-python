import pytest
from pydantic import BaseModel, ValidationError

from clabe import BANK_NAMES, BANKS
from clabe.types import Clabe

VALID_CLABE = '723123456682660854'


class Cuenta(BaseModel):
    clabe: Clabe


def test_valid_clabe():
    cuenta = Cuenta(clabe=VALID_CLABE)
    assert cuenta.clabe.bank_code_abm == '723'
    assert cuenta.clabe.bank_code_banxico == BANKS['723']
    assert cuenta.clabe.bank_name == BANK_NAMES[BANKS['723']]
    assert cuenta.clabe.bank_code == cuenta.clabe.bank_code_banxico


@pytest.mark.parametrize(
    'clabe,expected_message',
    [
        pytest.param(
            'h' * 18,
            'debe ser numérico',
            id='clabe_not_digit',
        ),
        pytest.param(
            '9' * 17,
            'String should have at least 18 characters',
            id='invalid_bank_length',
        ),
        pytest.param(
            '9' * 19,
            'String should have at most 18 characters',
            id='invalid_bank_length',
        ),
        pytest.param(
            '111180157042875763',
            'código de banco no es válido',
            id='invalid_bank_code',
        ),
        pytest.param(
            '001' + '9' * 15,
            'clabe dígito de control no es válido',
            id='invalid_control_digit',
        ),
    ],
)
def test_invalid_clabe(clabe: Clabe, expected_message: str) -> None:
    with pytest.raises(ValidationError) as exc:
        Cuenta(clabe=clabe)
    assert expected_message in str(exc.value)


def test_get_json_schema() -> None:
    from pydantic import TypeAdapter

    adapter = TypeAdapter(Clabe)
    schema = adapter.json_schema()
    assert schema == {
        'description': 'CLABE (Clave Bancaria Estandarizada)',
        'examples': ['723010123456789019'],
        'maxLength': 18,
        'minLength': 18,
        'pattern': '^[0-9]{18}$',
        'type': 'string',
    }
