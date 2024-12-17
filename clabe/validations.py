import random
from typing import List, Union

from pydantic_core import PydanticCustomError

from .banks import BANK_NAMES, BANKS

CLABE_LENGTH = 18
CLABE_WEIGHTS = [3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7]


def compute_control_digit(clabe: Union[str, List[int]]) -> str:
    """
    Compute CLABE control digit according to
    https://es.wikipedia.org/wiki/CLABE#D.C3.ADgito_control
    """
    clabe = [int(i) for i in clabe]
    weighted = [
        c * w % 10 for c, w in zip(clabe[: CLABE_LENGTH - 1], CLABE_WEIGHTS)
    ]
    summed = sum(weighted) % 10
    control_digit = (10 - summed) % 10
    return str(control_digit)


def validate_clabe(clabe: str) -> bool:
    """
    Validate CLABE according to
    https://es.wikipedia.org/wiki/CLABE#D.C3.ADgito_control
    """
    return (
        clabe.isdigit()
        and len(clabe) == CLABE_LENGTH
        and clabe[:3] in BANKS.keys()
        and clabe[-1] == compute_control_digit(clabe)
    )


def get_bank_name(clabe: str) -> str:
    """
    Regresa el nombre del banco basado en los primeros 3 digitos
    https://es.wikipedia.org/wiki/CLABE#D.C3.ADgito_control
    """
    code = clabe[:3]
    try:
        bank_name = BANK_NAMES[BANKS[code]]
    except KeyError:
        raise ValueError(f"Ningún banco tiene código '{code}'")
    else:
        return bank_name


def generate_new_clabes(number_of_clabes: int, prefix: str) -> List[str]:
    clabes = []
    missing = CLABE_LENGTH - len(prefix) - 1
    assert (10**missing - 10 ** (missing - 1)) >= number_of_clabes
    clabe_sections = random.sample(
        range(10 ** (missing - 1), 10**missing), number_of_clabes
    )
    for clabe_section in clabe_sections:
        clabe = prefix + str(clabe_section)
        clabe += compute_control_digit(clabe)
        assert validate_clabe(clabe)
        clabes.append(clabe)
    return clabes


def configure_additional_bank(
    bank_code_abm: str, bank_code_banxico: str, bank_name: str
) -> None:
    """
    Configures an additional bank.

    Args:
        bank_code_abm (str): The ABM code for the bank.
        bank_code_banxico (str): The Banxico code for the bank.
        bank_name (str): The name of the bank.

    Raises:
        ValueError: If the bank_code_abm or bank_code_banxico
        already exists in the provided dictionaries.
    """

    if not all(
        isinstance(x, str)
        for x in [bank_code_abm, bank_code_banxico, bank_name]
    ):
        raise TypeError('All parameters must be strings')

    if not bank_code_abm.isdigit():
        raise TypeError('debe ser numérico')

    if not bank_code_banxico.isdigit():
        raise TypeError('debe ser numérico')

    if not bank_name.strip():
        raise ValueError('bank_name cannot be empty')

    if bank_code_abm in BANKS:
        raise PydanticCustomError(
            'clabe.bank_code_abm', 'código de banco ABM ya existe'
        )

    if bank_code_banxico in BANK_NAMES:
        raise PydanticCustomError(
            'clabe.bank_code_banxico', 'código de banco banxico ya existe'
        )

    BANKS[bank_code_abm] = bank_code_banxico
    BANK_NAMES[bank_code_banxico] = bank_name.strip()
