import pytest

from clabe import (
    compute_control_digit,
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
