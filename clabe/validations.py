import random
import re
from typing import List, Union

from pydantic import BaseModel, Field, validator

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
    bank_name: str = Field(
        min_length=1,
        strip_whitespace=True,
        description="The name of the bank - cannot be empty",
    )

    bank_code_banxico: str = Field(
        min_length=5, max_length=5, description="The Banxico code for the bank"
    )

    @validator("bank_code_banxico")
    def validate_bank_code(cls, value):
        if not re.fullmatch(r"\d{5}", value):
            raise ValueError(
                "bank_code_banxico must be a string of exactly 5 digits"
            )
        return value

    @property
    def bank_code_abm(self):
        return self.bank_code_banxico[-3:]


def configure_additional_bank(bank_code_banxico: str, bank_name: str) -> None:

    request = BankConfigRequest(
        bank_code_banxico=bank_code_banxico,
        bank_name=bank_name,
    )
    BANKS[request.bank_code_abm] = request.bank_code_banxico
    BANK_NAMES[request.bank_code_banxico] = request.bank_name
