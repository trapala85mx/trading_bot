# Python
from abc import ABCMeta, abstractmethod
from typing import Callable
# Project


class BaseExchange(metaclass=ABCMeta):
    """Abstract Class that defines what an Exchange must have
    """

    def __init__(self, api_key: str, api_secret: str):
        self._api_key: str = api_key
        self._api_secret: str = api_secret
        self._hedge_mode: bool | None = None

    @property
    @abstractmethod
    def hedge_mode(self): pass

    # Public Endopoints
    @abstractmethod
    async def get_klines(self, symbol: str, interval: str, start=None, end=None, limit: int = 500):
        """Extract the kline data from an Exchange. By default retrieves the las 500 klines
        but it could be from an range of time

        Args:
            symbol (str): symbol to retrueve data from exchange
            interval (str): klines interval to retrive info
            start ([timestamp], optional): Start timestamp to initiate retrieving klines. Defaults to None 
            end ([timestamp], optional): End timestamoo ti finish retrieving data. Defaults to None.
            limit (int, optional): How many candle to retrieve from exchange. Defaults to 500.
        """
        pass

    @abstractmethod
    async def get_exchange_info(self, symbol: str | None = None, **kwargs):
        """Get exchange info where all cryptos are listed or get just info from specific symbol

        Args:
            symbol (str, optional): Crypto to retrieve info. Defaults to None to retrieve all info for all cryptos in exchange
        """
        pass

    @abstractmethod
    async def close_connection(self):
        """Close a client connection to close connection with exchange
        """
        pass

    # Websockets Endpoints
    @abstractmethod
    async def kline_socket(self, symbol: str, timeframe: str, callback: Callable):
        """Create a websocket that receives kline data from specific symbol an interval

        Args:
            symbol (str): symbol to retrieve data
            timeframe (str): timeframe for klines
            callback (Callable): function to process websocket message
        """
        pass

    @abstractmethod
    async def user_socket(self, callback: Callable):
        pass

    # Account Endpoints
    @abstractmethod
    async def create_buy_market_order(self, params:dict) -> dict:
        pass
    
    @abstractmethod
    async def create_sell_market_order(self, params:dict):
        pass

    @abstractmethod
    async def create_buy_limit_order(self, params:dict):
        pass

    @abstractmethod
    async def create_sell_limit_order(self, params:dict):
        pass

    @abstractmethod
    async def set_stop_loss_for_long_position(self, params:dict):
        pass

    @abstractmethod
    async def set_stop_loss_for_short_position(self, params: dict):
        pass

    @abstractmethod
    async def set_take_profit_for_long_position_in_hedge_mode(self, params: dict):
        pass

    @abstractmethod
    async def set_take_profit_for_short_position_in_hedge_mode(self, params: dict):
        pass

    @abstractmethod
    async def get_current_position_mode(self):
        pass
