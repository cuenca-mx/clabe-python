import pydantic


def is_pydantic_v1_installed() -> bool:
    return pydantic.VERSION.startswith('1.')