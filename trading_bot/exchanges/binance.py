# Pyhton
from decimal import Decimal
# Project
from typing import Callable
from abstracts.exchange import BaseExchange
from utils.decorators import only_kwargs
# Third party
from binance import AsyncClient, BinanceSocketManager


class Binance(BaseExchange):
    """Class that implements Abstract Class BaseExchange and implements according to Binance Exchange API information
    """    
    def __init__(self, api_key: str, api_secret: str):
        super().__init__(api_key=api_key, api_secret=api_secret)
        # self._api_key = api_key
        # self._api_secret = api_secret
        self._client: AsyncClient | None = None
        self._bsm: BinanceSocketManager | None = None

    @property
    def hedge_mode(self):
        return self._hedge_mode

    async def _create_client(self):
        """Creates a client to comunicate with Binance Exchange
        """        
        if not self._client:
            self._client = await AsyncClient.create(
                api_key=self._api_key, api_secret=self._api_secret
            )
        return

    async def _crete_socket_manager(self):
        """Creates a BinanceSocketManaget for websocket comunication
        """        
        await self._create_client()
        if not self._bsm:
            self._bsm = BinanceSocketManager(self._client)
        return self._bsm

    async def get_klines(
            self, symbol: str, interval: str, start=None, end=None, limit: int = 500
    ) -> list[list]:
        """Get klines from Binance Exchange

        Args:
            symbol (str): crypto to get the klines
            interval (str): Timeframe/interval of the klines
            start (Timestamp, optional): from when should start retrieving klines. Defaults to None.
            end (Timestamp, optional): from whe should end retrieving klines. Defaults to None.
            limit (int, optional): How many klines to retireve. Defaults to 500.

        Returns:
            [list[list]]: list that contains all klines, where each kline is a list
        """        
        await self._create_client()
        if start is None or end is None:
            return await self._client.futures_klines(
                symbol=symbol.lower(), interval=interval, limit=limit
            )

        if not (start is None) and not (end is None):
            return await self._client.futures_klines(
                symbol=symbol.lower(),
                interval=interval,
                start=start,
                end=end,
                limit=limit,
            )

    async def get_exchange_info(
            self, category: str = "linear", symbol: str | None = None
    ) -> dict:
        """Get the exchange info for one symbol or all the symbols in exchange

        Args:
            category (str, optional): Not needed here. Defaults to "linear".
            symbol (str, optional): Symbol to look for information in exchange. Defaults to None.

        Returns:
            dict: Dictionary with all exchange info for the symbol or all the symbols in exchange
        """        
        await self._create_client()
        if symbol is None:
            return await self._client.futures_exchange_info()
        return await self._client.get_symbol_info(symbol=symbol)

    async def kline_socket(self, symbol: str, timeframe: str, callback: Callable):
        """Starts websocket for klies in Binance Exchange

        Args:
            symbol (str): symbol to liste for messages
            timeframe (str): interval of the klines
            callback (Callable): Function that will process te message received
        """        
        await self._crete_socket_manager()
        kline_socket = self._bsm.kline_futures_socket(symbol=symbol, interval=timeframe)
        async with kline_socket as ks:
            while True:
                res = await ks.recv()
                await callback(res)

    async def user_socket(self, callback: Callable):
        """Start a user socket for binance exchange

        Args:
            callback (Callable): Functin to procees the message received
        """        
        await self._crete_socket_manager()
        user_stream = self._bsm.futures_user_socket()
        async with user_stream as us:
            while True:
                res = await us.recv()
                await callback(res)

    async def close_connection(self):
        """Closes conncetion to binance exchange
        """        
        if self._client:
            await self._client.close_connection()
            self._client = None

    async def get_current_position_mode(self):
        """Gets the curren hedge mode setted in exchange

        Raises:
            ValueError: If couldn´t get the position mode
        """        
        await self._create_client()
        result = await self._client.futures_get_position_mode()
        result = result.get("dualSidePosition", None)
        if result is None:
            raise ValueError("Couldn't get current dual position")
        self._hedge_mode = result

    @only_kwargs
    async def create_buy_market_order(self, params: dict) -> dict:
        """Creates a buy market order decorated with only_kwars to just use kwargs in passing arguments

        Args:
            params (dict): Dictionary with order information

        Returns:
            dict: dictionary with the order params sent it to Binance
        
        TO DO:
            change function params to params to just needed variables such a symbol, etc.
        """        
        side = "BUY"
        await self._create_client()
        resp = await self._client.futures_create_order(
            symbol=params["symbol"].upper(),
            side=side,
            positionSide=await self._set_position_side_for_hedge_mode(side=side),
            type="MARKET",
            quantity=Decimal(params["quantity"])
        )
        return resp

    @only_kwargs
    async def create_sell_market_order(self, params: dict):
        """Creates a sell market order decorated with only_kwars to just use kwargs in passing arguments

        Args:
            params (dict): Dictionary with order information

        Returns:
            dict: dictionary with the order params sent it to Binance
        
        TO DO:
            change function params to params to just needed variables such a symbol, etc.
        """
        side = "SELL"
        await self._create_client()
        resp = await self._client.futures_create_order(
            symbol=params["symbol"].upper(),
            side=side,
            positionSide=await self._set_position_side_for_hedge_mode(side=side),
            type="MARKET",
            quantity=Decimal(params["quantity"])
        )
        return resp

    @only_kwargs
    async def create_buy_limit_order(self, params: dict):
        """Creates a buy limit order decorated with only_kwars to just use kwargs in passing arguments

        Args:
            params (dict): Dictionary with order information

        Returns:
            dict: dictionary with the order params sent it to Binance
        
        TO DO:
            change function params to params to just needed variables such a symbol, etc.
        """
        side = "BUY"
        await self._create_client()
        resp = await self._client.futures_create_order(
            type="LIMIT",
            symbol=params["symbol"],
            price=Decimal(params["entry_price"]),
            quantity=Decimal(params["quantity"]),
            side=side,
            positionSide=await self._set_position_side_for_hedge_mode(side=side),
            timeInForce="GTC"
        )
        return resp

    @only_kwargs
    async def create_sell_limit_order(self, params: dict):
        """Creates a sell limit order decorated with only_kwars to just use kwargs in passing arguments

        Args:
            params (dict): Dictionary with order information

        Returns:
            dict: dictionary with the order params sent it to Binance
        
        TO DO:
            change function params to params to just needed variables such a symbol, etc.
        """
        side = "SELL"
        await self._create_client()
        resp = await self._client.futures_create_order(
            type="LIMIT",
            symbol=params["symbol"],
            price=Decimal(params["entry_price"]),
            quantity=Decimal(params["quantity"]),
            side=side,
            positionSide=await self._set_position_side_for_hedge_mode(side=side),
            timeInForce="GTC"
        )
        return resp

    @only_kwargs
    async def set_stop_loss_for_long_position(self, params: dict):
        """Creates a stop loss market order for long positions decorated with only_kwars to just use kwargs in passing arguments

        Args:
            params (dict): Dictionary with order information

        Returns:
            dict: dictionary with the order params sent it to Binance
        
        TO DO:
            change function params to params to just needed variables such a symbol, etc.
        """
        side = "SELL"
        await self._create_client()
        resp = await self._client.futures_create_order(
            type="STOP_MARKET",
            symbol=params["symbol"],
            side=side,
            stopPrice=params["stop_loss_price"],
            closePosition=True,
            positionSide=await self._set_position_side_for_hedge_mode(side="BUY"),
        )
        return resp

    @only_kwargs
    async def set_stop_loss_for_short_position(self, params: dict):
        """Creates a stop loss market order for short positions decorated with only_kwars to just use kwargs in passing arguments

        Args:
            params (dict): Dictionary with order information

        Returns:
            dict: dictionary with the order params sent it to Binance
        
        TO DO:
            change function params to params to just needed variables such a symbol, etc.
        """
        side = "BUY"
        await self._create_client()
        resp = await self._client.futures_create_order(
            type="STOP_MARKET",
            symbol=params["symbol"],
            side=side,
            stopPrice=params["stop_loss_price"],
            closePosition=True,
            positionSide=await self._set_position_side_for_hedge_mode(side="SELL"),
        )
        return resp

    @only_kwargs
    async def set_take_profit_for_long_position_in_hedge_mode(self, params: dict):
        """Creates a Take Profit Limit order for long positions decorated with only_kwars to just use kwargs in passing arguments

        Args:
            params (dict): Dictionary with order information

        Returns:
            dict: dictionary with the order params sent it to Binance
        
        TO DO:
            change function params to params to just needed variables such a symbol, etc.
        """
        side = "SELL"
        await self._create_client()
        resp = await self._client.futures_create_order(
            type="LIMIT",
            symbol=params["symbol"],
            price=params["stop_loss_price"],
            side=side,
            quantity=params['quantity'],
            positionSide=await self._set_position_side_for_hedge_mode(side="BUY"),
            timeInForce="GTC"
        )
        return resp

    @only_kwargs
    async def set_take_profit_for_short_position_in_hedge_mode(self, params: dict):
        """Creates a Take Profit Limit order for Short positions decorated with only_kwars to just use kwargs in passing arguments

        Args:
            params (dict): Dictionary with order information

        Returns:
            dict: dictionary with the order params sent it to Binance
        
        TO DO:
            change function params to params to just needed variables such a symbol, etc.
        """
        side = "BUY"
        await self._create_client()
        resp = await self._client.futures_create_order(
            type="LIMIT",
            symbol=params["symbol"],
            price=params["stop_loss_price"],
            side=side,
            quantity=params['quantity'],
            positionSide=await self._set_position_side_for_hedge_mode(side="SELL"),
            timeInForce="GTC"
        )
        return resp

    # METHODS
    async def _set_position_side_for_hedge_mode(self, side: str) -> str:
        """Sets position side if hedge mode is activated

        Args:
            side (str): Position Side

        Returns:
            str: positionSide variable needed for sending orders into Binane Exchange
        """        
        if self._hedge_mode and side == "BUY":
            return "LONG"

        if self._hedge_mode and side == "SELL":
            return "SHORT"

        if not self._hedge_mode:
            return "BOTH"
