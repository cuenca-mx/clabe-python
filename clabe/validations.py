import random
from typing import List, Union

from pydantic import BaseModel, Field

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


class BankConfigRequest(BaseModel):
    """
    Validates and processes bank configuration requests.

    The class handles validation of bank names and codes, ensuring:
    - Bank names are non-empty strings
    - Banxico codes are exactly 5 digits
    """

    bank_name: str = Field(
        min_length=1,
        strip_whitespace=True,
        description="Bank name must have at least 1 character.",
    )

    bank_code_banxico: str = Field(
        regex=r"^\d{5}$", description="Banxico code must be a 5-digit string."
    )

    @property
    def bank_code_abm(self):
        return self.bank_code_banxico[-3:]


def add_bank(bank_code_banxico: str, bank_name: str) -> None:
    """
    Add a bank configuration.

    Args:
        bank_code_banxico: 5-digit Banxico bank code
        bank_name: Bank name
    """
    request = BankConfigRequest(
        bank_code_banxico=bank_code_banxico,
        bank_name=bank_name,
    )
    BANKS[request.bank_code_abm] = request.bank_code_banxico
    BANK_NAMES[request.bank_code_banxico] = request.bank_name


def remove_bank(bank_code_banxico: str) -> None:
    """
    Remove a bank configuration by its Banxico code.

    Args:
        bank_code_banxico: 5-digit Banxico bank code
    """
    BANKS.pop(bank_code_banxico[-3:], None)
    BANK_NAMES.pop(bank_code_banxico, None)
