# Python
import functools
# Project
from .errors import KwargsOnlyError
# Externals


def only_kwargs(func):
    """Decorator to check that we are passing only kwargs arguments

    Args:
        func ([type]): function to be decorated

    Raises:
        KwargsOnlyError: If is passed args into the params of the function

    Returns:
        Callable: the funciton validated
    """    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) > 1:
            raise KwargsOnlyError("Only kwargs argumetns allowed")
        return func(*args, **kwargs)
    return wrapper