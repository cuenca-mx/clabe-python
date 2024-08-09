import pydantic


def is_pydantic_v1():
    return pydantic.VERSION.startswith('1.')
