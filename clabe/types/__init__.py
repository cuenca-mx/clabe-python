import pydantic

from ..utils import pydantic_v1

if pydantic_v1():
    from .clabes_legacy.clabes import Clabe, validate_digits
else:
    from .clabes import Clabe
