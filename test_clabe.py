import clabe


VALID_CLABE = '032180000118359719'
INVALID_CLABE = '032180000118359711'


def test_compute_control_digit():
    assert clabe.compute_control_digit(VALID_CLABE[:17]) == VALID_CLABE[17]


def test_validate_clabe():
    assert clabe.validate_clabe(VALID_CLABE)
    assert not clabe.validate_clabe(INVALID_CLABE)


def test_get_bank_name():
    assert clabe.get_bank_name('002') == clabe.BankCode.BANAMEX
    assert clabe.get_bank_name('989') is None
    assert clabe.get_bank_name('99999999') is None
