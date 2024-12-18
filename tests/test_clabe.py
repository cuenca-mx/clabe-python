import pytest

from clabe import (
    compute_control_digit,
    configure_additional_bank,
    generate_new_clabes,
    get_bank_name,
    validate_clabe,
)

VALID_CLABE = '002000000000000008'
INVALID_CLABE_CONTROL_DIGIT = '002000000000000007'
INVALID_CLABE_BANK_CODE = '0' * 18  # Control digit es valido


def test_compute_control_digit():
    assert compute_control_digit(VALID_CLABE[:17]) == VALID_CLABE[17]


def test_validate_clabe():
    assert validate_clabe(VALID_CLABE)
    assert not validate_clabe(INVALID_CLABE_BANK_CODE)
    assert not validate_clabe(INVALID_CLABE_CONTROL_DIGIT)


def test_get_bank_name():
    assert get_bank_name('002') == 'Banamex'
    with pytest.raises(ValueError):
        get_bank_name('989')


def test_generate_new_clabes():
    num_clabes = 10
    prefix = '64618000011'
    clabes = generate_new_clabes(10, prefix)
    assert len(clabes) == num_clabes
    for clabe in clabes:
        assert clabe.startswith(prefix)
        assert validate_clabe(clabe)


@pytest.mark.parametrize(
    'abm_code, banxico_code, name',
    [
        ('713', '90713', 'Cuenca DMZ'),
        ('777', '713', 'Cuenca Gem DMZ'),
        ('666', '723', 'Cuenca Gem Beta'),
    ],
)
def test_configure_additional_bank_success(abm_code, banxico_code, name):
    configure_additional_bank(abm_code, banxico_code, name)
    assert get_bank_name(abm_code) == name


@pytest.mark.parametrize(
    'abm_code, banxico_code, name',
    [
        ('A', 'B', 'C'),  # Invalid format for both codes
        ('666', 'B', 'Test Bank'),  # Valid ABM code, invalid Banxico code
        ('777', '713', ''),  # Valid codes, empty name
        ('abc', 'def', 'Test Bank'),  # Non-numeric codes
    ],
)
def test_configure_additional_bank_invalid_inputs(
    abm_code, banxico_code, name
):
    with pytest.raises(ValueError):
        configure_additional_bank(abm_code, banxico_code, name)
