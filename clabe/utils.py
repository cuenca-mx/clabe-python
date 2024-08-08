import pydantic


def pydantic_v1():
    return pydantic.VERSION.startswith('1.')
