import pydantic


def is_pydantic_v1() -> bool:
    return pydantic.VERSION.startswith('1.')
