class KwargsOnlyError(Exception):
    """Class that represents a Custom Error when args are passed
    """    
    def __init__(self, msg:str) -> None:
        self._msg = msg
    
    def __str__(self):
        return f"KwargsOnlyError: {self._msg}"