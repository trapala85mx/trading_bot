# Pyhton
import asyncio
# Project
from typing import Callable, List
from . import BaseExchange
# Third party
from binance import AsyncClient, BinanceSocketManager
from binance import enums

from ..models import Order


class Binance(BaseExchange):

    def __init__(self, api_key: str, api_secret: str):
        super().__init__(api_key=api_key, api_secret=api_secret)
        self._api_key = api_key
        self._api_secret = api_secret
        self._client: AsyncClient | None = None
        self._bsm: BinanceSocketManager | None = None

    async def _create_client(self):
        if not self._client:
            self._client = await AsyncClient.create(api_key=self._api_key, api_secret=self._api_secret)

        return

    async def _crete_socket_manager(self):
        await self._create_client()
        if not self._bsm:
            self._bsm = BinanceSocketManager(self._client)
        return self._bsm

    async def get_klines(self, symbol: str, interval: str, start=None, end=None, limit: int = 500):
        await self._create_client()
        if start is None or end is None:
            return await self._client.futures_klines(symbol=symbol.lower(), interval=interval, limit=limit)

        if not (start is None) and not (end is None):
            return await self._client.futures_klines(symbol=symbol.lower(), interval=interval,
                                               start=start, end=end, limit=limit)

    async def get_exchange_info(self, category: str = "linear", symbol: str | None = None):
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
        await  self._crete_socket_manager()
        user_stream = self._bsm.futures_user_socket()
        async with user_stream as us:
            while True:
                res = await us.recv()
                await callback(res)

    async def close_connection(self):
        if self._client:
            await self._client.close_connection()
            self._client = None

