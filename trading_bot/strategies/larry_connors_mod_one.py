# Python
import asyncio

# Project
from models.asset import Asset

from abstracts.strategy import Strategy
from abstracts.exchange import BaseExchange

from utils.indicators import rsi, ma
from utils.data_format import update_dataframe
from utils.data_format import create_dataframe, create_candle_dataframe
from utils.telegram_notifier import TelegramNotifier

# Externals
import binance.enums as tf
import pandas as pd


class LarryConnorsModOneStrategy(Strategy):
    """Class that has all the logc for Larry Connors Strategy using the Notifier class to send signals
    """    
    def __init__(self, asset: Asset, exchange: BaseExchange):
        super().__init__(asset, exchange)
        self._snapshot_h4 = None
        self._position_open = False
        self._position_side = False
        

    async def _get_indicators(self):
        """Create indicatros needed
        """        
        tasks = []
        tasks.append(asyncio.create_task(rsi(self._snapshot_h4["close"], period=2)))
        tasks.append(
            asyncio.create_task(
                ma(
                    self._snapshot_h4["close"],
                    precision=int(self._asset.price_precision),
                    period=265,
                )
            )
        )
        tasks.append(
            asyncio.create_task(
                ma(
                    self._snapshot_h4["close"],
                    precision=int(self._asset.price_precision),
                    period=11,
                )
            )
        )

        (
            self._snapshot_h4["rsi"],
            self._snapshot_h4["ma265"],
            self._snapshot_h4["ma11"],
        ) = await asyncio.gather(*tasks)

    async def _snapshot(self) -> pd.DataFrame:
        """Creates snapshot using exchange

        Returns:
            [pd.DataFrame]: DataFrame of the snapshot
        """        
        data = await self._exchange.get_klines(
            symbol=self._asset.symbol,
            interval=tf.KLINE_INTERVAL_4HOUR
            #interval=tf.KLINE_INTERVAL_1MINUTE,
        )
        data = await create_dataframe(data)
        return data

    async def _analyze_data(self):
        """Analyze the data and send signal
        
            TO DO:
                Inseatd of sending signal will open orders and send the signal when an order is sent and opened
        """        
        previous_rsi = self._snapshot_h4["rsi"].iloc[-2]
        rsi = self._snapshot_h4["rsi"].iloc[-1]
        ma11 = self._snapshot_h4["ma11"].iloc[-1]
        ma265 = self._snapshot_h4["ma265"].iloc[-1]
        close = self._snapshot_h4["close"].iloc[-1]
        
        if not self._position_open:
            # BUY SIGNAL
            if close > ma265:
                if close < ma11 and previous_rsi < 9 and rsi > 9:
                    print(f"{'*' * 50}LONG - {self._asset.symbol.upper()}\{'*' * 50}")
                    print("Ejecutando compra")
                    self._position_open = True
                    self._position_side = "LONG"
                    msg = f"{'*'*50}\n🟢 LONG \n{self._asset.symbol.upper()} ${close}\n{'*'*50}"
                    print(msg)
                    await TelegramNotifier.send_message(msg=msg)
                    

            # SELL SIGNAL
            if close < ma265:
                if close > ma11 and previous_rsi > 74 and rsi < 74:
                    print(f"{'*' * 50} SELL - {self._asset.symbol.upper()} {'*' * 50}")
                    print("Ejecutando Venta")
                    self._position_open = True
                    self._position_side = "SHORT"
                    msg = f"{'*'*50}\n🔴 SHORT\n{self._asset.symbol.upper()} ${close}\n{'*'*50}"
                    print(msg)
                    await TelegramNotifier.send_message(msg=msg)
        
        else:
            # Here we have Position Open, so we need to close it
            
            # Close Long
            if self._position_side == "LONG":
                if close > ma11:
                    print(f"{'*' * 50} Cerrando LONG {'*' * 50}")
                    print("Posición Cerrada")
                    self._position_open = False
                    self._position_side = ""
                    msg = f"{'*'*50}CERRAR LONG\n{self._asset.symbol.upper()}\n{close}\n{'*'*50}"
                    print(msg)
                    await TelegramNotifier.send_message(msg=msg)
            
            # Close Short
            if self._position_side == "SHORT":
                if close < ma11:
                    print(f"{'*' * 50} Cerrando SHORT {'*' * 50}")
                    print("Posición Cerrada")
                    self._position_open = False
                    self._position_side = ""
                    msg = f"{'*'*50}LONG\n{self._asset.symbol.upper()}\n{close}\n{'*'*50}"
                    print(msg)
                    await TelegramNotifier.send_message(msg=msg)
        

    async def _process_data(self, msg: dict):
        """Porcess the meesage recevided from websocket to just filter the data needed for analyze

        Args:
            msg (dict): Message from websocket
        """        
        if msg.get("e"):
            candle = msg.get("k")
            if candle.get("x"):
                candle = await create_candle_dataframe(candle)
                self._snapshot_h4 = await update_dataframe(self._snapshot_h4, candle)
                await self._get_indicators()
                await self._analyze_data()

    async def _setup_strategy(self):
        """retrieves the information needed for the Strategy
        """        
        self._snapshot_h4 = await self._snapshot()
        await self._get_indicators()

    async def start(self):
        """Starts the strategy
        """        
        print("Setting up Strategy")
        print("Starting")
        await self._setup_strategy()
        await self._analyze_data()
        await self._exchange.kline_socket(
            symbol=self._asset.symbol, timeframe=tf.KLINE_INTERVAL_4HOUR, callback=self._process_data
        )
