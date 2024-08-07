import pydantic

if pydantic.VERSION.startswith('1.'):
    from .clabes_legacy.clabes import Clabe, validate_digits
else:
    from .clabes import Clabe, validate_digits
