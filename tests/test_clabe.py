import pytest

from clabe import (
    BANK_NAMES,
    BANKS,
    add_bank,
    compute_control_digit,
    generate_new_clabes,
    get_bank_name,
    remove_bank,
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
        ('714', '90714', 'Cuenca Gem DMZ'),
        ('715', '90715', 'Cuenca Gem Beta'),
    ],
)
def test_add_bank_success(abm_code, banxico_code, name):
    add_bank(banxico_code, name)
    assert get_bank_name(abm_code) == name


@pytest.mark.parametrize(
    'banxico_code, name',
    [
        ('1234', 'Test Bank'),  # invalid Banxico code 4 digits
        ('123456', 'Test Bank'),  # invalid Banxico code 6 digits
        ('12345', ''),  # Valid code, empty name
        ('123AT', 'Test Bank'),  # Non-numeric codes
    ],
)
def test_add_bank_invalid_inputs(banxico_code, name):
    with pytest.raises(ValueError):
        add_bank(banxico_code, name)


def test_remove_bank():
    test_code = "90716"
    test_name = "To Delete Bank"
    add_bank(test_code, test_name)

    assert test_code[-3:] in BANKS
    assert test_code in BANK_NAMES

    remove_bank(test_code)

    assert test_code[-3:] not in BANKS
    assert test_code not in BANK_NAMES


def test_remove_nonexistent_bank():
    nonexistent_code = "99999"

    remove_bank(nonexistent_code)

    assert nonexistent_code[-3:] not in BANKS
    assert nonexistent_code not in BANK_NAMES
