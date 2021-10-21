# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from typing import TypeVar, Callable, Coroutine, Any, Union, Literal


class MissingType:
    """Type class for missing attributes and parameters."""

    def __repr__(self):
        return "<MISSING>"

    def __bool__(self) -> bool:
        return False


MISSING = MissingType()


T = TypeVar('T')


APINullable = Union[T, MissingType]


Coro = TypeVar("Coro", bound=Callable[..., Coroutine[Any, Any, Any]])


Choices = Literal


choice_value_types = (str, int, float)


class Singleton(type):
    # Thanks to this stackoverflow answer (method 3):
    # https://stackoverflow.com/q/6760685/12668716
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton,
                cls
            ).__call__(*args, **kwargs)
        return cls._instances[cls]
