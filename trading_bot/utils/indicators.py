import talib as ta
import pandas as pd


async def rsi(src: pd.Series, period: int = 14):
    return round(ta.RSI(src, timeperiod=period), 2)


async def ma(src: pd.Series, precision: int, period: int = 265):
    return round(ta.MA(src, timeperiod=period), precision)


async def atr(high: pd.Series, low: pd.Series, close: pd.Series, precision: int, period: int = 14):
    return round(ta.ATR(high=high, low=low, close=close, timeperiod=period), precision)
