from abc import ABC, abstractmethod


class Notifier(ABC):
    """Abstract Class that represents any Notifire in charge to send signal
    """    
    @classmethod
    @abstractmethod
    async def send_message(cls, msg:str):
        pass