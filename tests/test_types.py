import pytest
from pydantic import BaseModel, ValidationError

from clabe import BANK_NAMES, BANKS
from clabe.types import Clabe
from clabe.utils import is_pydantic_v1

VALID_CLABE = '646180157042875763'


class Cuenta(BaseModel):
    clabe: Clabe


def test_valid_clabe():
    cuenta = Cuenta(clabe=VALID_CLABE)
    assert cuenta.clabe.bank_code_abm == '646'
    assert cuenta.clabe.bank_code_banxico == BANKS['646']
    assert cuenta.clabe.bank_name == BANK_NAMES[BANKS['646']]
    assert cuenta.clabe.bank_code == cuenta.clabe.bank_code_banxico


@pytest.mark.parametrize(
    'clabe,expected_message',
    [
        pytest.param(
            'h' * 18,
            'card number is not all digits',
            marks=pytest.mark.skipif(
                not is_pydantic_v1(), reason='only pydantic v1'
            ),
            id='non_numeric_pydantic_v1',
        ),
        pytest.param(
            'h' * 18,
            'debe ser numérico',
            marks=pytest.mark.skipif(
                is_pydantic_v1(), reason='only pydantic v2'
            ),
            id='non_numeric_pydantic_v2',
        ),
        pytest.param(
            '9' * 17,
            'ensure this value has at least 18 characters',
            marks=pytest.mark.skipif(
                not is_pydantic_v1(), reason='only pydantic v1'
            ),
            id='invalid_length_pydantic_v1',
        ),
        pytest.param(
            '9' * 17,
            'String should have at least 18 characters',
            marks=pytest.mark.skipif(
                is_pydantic_v1(), reason='only pydantic v2'
            ),
            id='invalid_length_pydantic_v2',
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
def test_invalid_clabe(clabe: str, expected_message: str) -> None:
    with pytest.raises(ValidationError) as exc:
        Cuenta(clabe=clabe)

    assert expected_message in str(exc.value)


@pytest.mark.skipif(is_pydantic_v1(), reason='only pydantic v2')
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
