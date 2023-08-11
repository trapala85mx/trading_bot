# Python
import asyncio
from decimal import Decimal
# Project
from models.market_order import MarketOrder
from exchanges.binance import Binance
# Third party
from decouple import config
import binance.enums as tf


async def process_message(msg: dict):
    print(msg)


async def main():
    print("Hola")
    # 1. Solicitar Estrategia a usar

    # 2. Solicitar Exchange a usar
    # Por el momento solo tenemos 1 estrategua y 1 exchange por lo que omitimos lo anterior

    # Creamos el objeto Exchange que será algo abstracto para que se iguale a lo que ingrese el usuario
    exchange = Binance(api_key=config("API_KEY"), api_secret=config("API_SECRET"))

    # Datos para ejemplo
    symbol = "maticusdt"
    interval = tf.KLINE_INTERVAL_15MINUTE

    try:
        # data = await exchange.get_klines(interval=interval, symbol=symbol)
        # data = await exchange.get_exchange_info() # sin symbol
        # data = await exchange.get_exchange_info(symbol=symbol)  # conn symbol
        # print(data)
        # await exchange.kline_socket(symbol=symbol, timeframe=interval, callback=process_message)
        # await exchange.user_socket(callback=process_message)
        market_order = MarketOrder(
            symbol="BTCUSD",
            position_side="LONG",
            position_type="MARGIN",
            qty=Decimal('0.1')
        )
        
        # La información que retorna solo es de la posición colocada más no de la posición abierta
        resp = await exchange.create_market_order(order=market_order)
        print(resp)

    except Exception as e:
        print(e)
    finally:
        await exchange.close_connection()


if __name__ == '__main__':
    asyncio.run(main())
