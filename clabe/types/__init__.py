from ..utils import is_pydantic_v1

__all__ = ['Clabe']

if is_pydantic_v1():
    from .clabes_legacy.clabes import Clabe  # type: ignore
else:
    from .clabes import Clabe  # type: ignore
