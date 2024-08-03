from ..helpers import is_pydantic_v1_installed

if is_pydantic_v1_installed():
    from .clabes_pydantic_v1 import Clabe, validate_digits
else:
    from .clabes import Clabe, validate_digits
