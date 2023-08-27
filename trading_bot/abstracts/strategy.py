from abc import ABC, abstractmethod

from abstracts.exchange import BaseExchange
from models.asset import Asset


class Strategy(ABC):
    """Abstract Class to represent a Base strategy
    """    
    def __init__(self, asset: Asset, exchange: BaseExchange):
        self._asset = asset
        self._exchange = exchange
        

    @abstractmethod
    async def _analyze_data(self):
        pass
    
    @abstractmethod
    async def _process_data(self, msg: dict):
        pass

    @abstractmethod
    async def _setup_strategy(self):
        pass

    @abstractmethod
    async def start(self):
        pass
