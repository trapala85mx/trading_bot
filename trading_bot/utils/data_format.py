# Python
# Project
# Externals
import pandas as pd


COLS = ["open_time", "open", "high", "low", "close", "volume"]


async def create_dataframe(data: list) -> pd.DataFrame:
    """Creates a DataFrame from a list. Basically used to create
       snapshot

    Args:
        data (list): List of Candles

    Returns:
        [pd.DataDrame]: a Dataframe of candles
    """    
    df: pd.DataFrame = pd.DataFrame(data)
    df = df.iloc[:, :6]
    df.columns = COLS
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["open"] = df["open"].astype("float")
    df["high"] = df["high"].astype("float")
    df["low"] = df["low"].astype("float")
    df["close"] = df["close"].astype("float")
    df["volume"] = df["volume"].astype("int")

    return df.iloc[:-1]

async def create_candle_dataframe(candle_dict: dict) -> pd.DataFrame:
    """Creates a DataFrame for a Candle

    Args:
        candle_dict (dict): candle data received from websocket in dictionary format

    Returns:
        pd.DataFrame: DataFrame for the candle
    """    
    candle = {
        "open_time": candle_dict["t"],
        "open": candle_dict["o"],
        "high": candle_dict["h"],
        "low": candle_dict["l"],
        "close": candle_dict["c"],
        "volume": candle_dict["v"]
    }
    df = pd.DataFrame([candle])
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["open"] = df["open"].astype("float")
    df["high"] = df["high"].astype("float")
    df["low"] = df["low"].astype("float")
    df["close"] = df["close"].astype("float")
    df["volume"] = df["volume"].astype("int")
    return df
    
async def update_dataframe(snapshot: pd.DataFrame, candle: pd.DataFrame) -> pd.DataFrame:
    """Update a Datafame and send the new data to the end of the dataframe

    Args:
        snapshot (pd.DataFrame): original data to be updated
        candle (pd.DataFrame): new data to update

    Returns:
        [pd.DataFrame]: The Dataframe updated
    """    
    df = pd.concat([snapshot, candle], ignore_index=True)
    return df.iloc[1:]
    