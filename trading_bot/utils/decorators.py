# Python
import functools
# Project
from .errors import KwargsOnlyError
# Externals


def only_kwargs(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) > 1:
            raise KwargsOnlyError("Only kwargs argumetns allowed")
        return func(*args, **kwargs)
    return wrapper