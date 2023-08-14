# Pyhton
from decimal import Decimal
# Project
from typing import Callable
from abstracts.exchange import BaseExchange
from utils.decorators import only_kwargs
# Third party
from binance import AsyncClient, BinanceSocketManager


class Binance(BaseExchange):
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
        if not self._client:
            self._client = await AsyncClient.create(
                api_key=self._api_key, api_secret=self._api_secret
            )
        return

    async def _crete_socket_manager(self):
        await self._create_client()
        if not self._bsm:
            self._bsm = BinanceSocketManager(self._client)
        return self._bsm

    async def get_klines(
            self, symbol: str, interval: str, start=None, end=None, limit: int = 500
    ):
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
    ):
        await self._create_client()
        if symbol is None:
            return await self._client.futures_exchange_info()
        return await self._client.get_symbol_info(symbol=symbol)

    async def kline_socket(self, symbol: str, timeframe: str, callback: Callable):
        await self._crete_socket_manager()
        kline_socket = self._bsm.kline_futures_socket(symbol=symbol, interval=timeframe)
        async with kline_socket as ks:
            while True:
                res = await ks.recv()
                await callback(res)

    async def user_socket(self, callback: Callable):
        await self._crete_socket_manager()
        user_stream = self._bsm.futures_user_socket()
        async with user_stream as us:
            while True:
                res = await us.recv()
                await callback(res)

    async def close_connection(self):
        if self._client:
            await self._client.close_connection()
            self._client = None

    async def get_current_position_mode(self):
        await self._create_client()
        result = await self._client.futures_get_position_mode()
        result = result.get("dualSidePosition", None)
        if result is None:
            raise ValueError("Couldn't get current dual position")
        self._hedge_mode = result

    @only_kwargs
    async def create_buy_market_order(self, params: dict) -> dict:
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

    async def create_buy_limit_order(self, params: dict):
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

    async def create_sell_limit_order(self, params: dict):
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

    async def set_stop_loss_for_long_position(self, params: dict):
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

    async def set_stop_loss_for_short_position(self, params: dict):
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

    async def set_take_profit_for_long_position_in_hedge_mode(self, params: dict):
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

    async def set_take_profit_for_short_position_in_hedge_mode(self, params: dict):
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
        if self._hedge_mode and side == "BUY":
            return "LONG"

        if self._hedge_mode and side == "SELL":
            return "SHORT"

        if not self._hedge_mode:
            return "BOTH"
