class KwargsOnlyError(Exception):
    def __init__(self, msg:str) -> None:
        self._msg = msg
    
    def __str__(self):
        return f"KwargsOnlyError: {self._msg}"