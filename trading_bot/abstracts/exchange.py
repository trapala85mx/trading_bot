# Python
from abc import ABCMeta, abstractmethod
from typing import Callable
# Project
# from ..models.order import Order
# from trading_bot import Order
from .order import Order


class BaseExchange(metaclass=ABCMeta):

    def __init__(self, api_key: str, api_secret: str):
        self._api_key = api_key
        self._api_secret = api_secret

    # Public Endopoints
    @abstractmethod
    async def get_klines(self, symbol: str, interval: str, start=None, end=None, limit: int = 500):
        pass

    @abstractmethod
    async def get_exchange_info(self, category: str = "linear", symbol: str | None = None):
        pass

    @abstractmethod
    async def close_connection(self):
        pass

    # Websockets Endpoints
    @abstractmethod
    async def kline_socket(self, symbol: str, timeframe: str, callback: Callable):
        pass

    @abstractmethod
    async def user_socket(self, callback: Callable):
        pass

    # Account Endpoints
    @abstractmethod
    async def create_market_order(self, order: Order):
        pass

    @abstractmethod
    async def create_limit_order(self, order: Order):
        pass

    @abstractmethod
    async def cancel_order(self, data: Order):
        pass

    @abstractmethod
    async def modify_order(self, data: Order):
        pass
