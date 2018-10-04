from clabe import (
    compute_control_digit, generate_new_clabes, get_bank_name, validate_clabe)


VALID_CLABE = '032180000118359719'
INVALID_CLABE = '032180000118359711'


def test_compute_control_digit():
    assert compute_control_digit(VALID_CLABE[:17]) == VALID_CLABE[17]


def test_validate_clabe():
    assert validate_clabe(VALID_CLABE)
    assert not validate_clabe(INVALID_CLABE)


def test_get_bank_name():
    assert get_bank_name('002') == 'BANAMEX'
    assert get_bank_name('989') is None
    assert get_bank_name('99999999') is None


def test_generate_new_clabes():
    num_clabes = 10
    prefix = '03218000011'
    clabes = generate_new_clabes(10, prefix)
    assert len(clabes) == num_clabes
    for clabe in clabes:
        assert clabe.startswith(prefix)
        assert validate_clabe(clabe)
