import clabe


VALID_CLABE = '032180000118359719'
INVALID_CLABE = '032180000118359711'


def test_compute_control_digit():
    assert clabe.compute_control_digit(VALID_CLABE[:17]) == VALID_CLABE[17]


def test_validate_clabe():
    assert clabe.validate_clabe(VALID_CLABE)
    assert not clabe.validate_clabe(INVALID_CLABE)
