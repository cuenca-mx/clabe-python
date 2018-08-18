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
            clabe[-1] == compute_control_digit(clabe))