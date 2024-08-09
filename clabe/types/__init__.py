import pydantic

from ..utils import is_pydantic_v1

if is_pydantic_v1():
    from .clabes_legacy.clabes import Clabe, validate_digits
else:
    from .clabes import Clabe
