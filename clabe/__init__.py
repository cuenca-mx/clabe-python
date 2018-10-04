import random
from typing import Union

from .banks import BankCode


CLABE_LENGTH = 18
CLABE_WEIGHTS = [3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7]


def compute_control_digit(clabe: str) -> str:
    """
    Compute CLABE control digit according to
    https://es.wikipedia.org/wiki/CLABE#D.C3.ADgito_control
    """
    clabe = [int(i) for i in clabe]
    weighted = [c * w % 10 for c, w in
                zip(clabe[:CLABE_LENGTH - 1], CLABE_WEIGHTS)]
    summed = sum(weighted) % 10
    control_digit = (10 - summed) % 10
    return str(control_digit)


def validate_clabe(clabe: str) -> bool:
    """
    Validate CLABE according to
    https://es.wikipedia.org/wiki/CLABE#D.C3.ADgito_control
    """
    return (clabe.isdigit() and
            len(clabe) == CLABE_LENGTH and
            get_bank_name(clabe[:3]) and
            clabe[-1] == compute_control_digit(clabe))


def get_bank_name(code: str) -> Union[str, None]:
    """
    Regresa el nombre del banco basado en los primeros 3 digitos
    https://es.wikipedia.org/wiki/CLABE#D.C3.ADgito_control
    :param code: Código de 3 digitos
    :return: Banco que corresponde al código, regresa None si no se encuentra
    """
    try:
        bank = BankCode(code)
    except ValueError:
        return None
    else:
        return bank.name


def generate_new_clabes(number_of_clabes, prefix):
    clabes = []
    missing = CLABE_LENGTH - len(prefix) - 1
    assert (10 ** missing - 10 ** (missing - 1)) >= number_of_clabes
    clabe_sections = random.sample(
        range(10 ** (missing - 1), 10 ** missing), number_of_clabes)
    for clabe_section in clabe_sections:
        clabe = prefix + str(clabe_section)
        clabe += compute_control_digit(clabe)
        assert validate_clabe(clabe)
        clabes.append(clabe)
    return clabes
