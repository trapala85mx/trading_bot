# Python
import asyncio
from decimal import Decimal
# Project
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
    symbol = "manausdt"
    interval = tf.KLINE_INTERVAL_15MINUTE
    
    try:
        # data = await exchange.get_klines(interval=interval, symbol=symbol)
        # data = await exchange.get_exchange_info() # sin symbol
        # data = await exchange.get_exchange_info(symbol=symbol)  # conn symbol
        # print(data)
        # await exchange.kline_socket(symbol=symbol, timeframe=interval, callback=process_message)
        # await exchange.user_socket(callback=process_message)

        # Probando extraer Exchange Mode - OK
        await exchange.get_current_position_mode()
        #print(exchange.hedge_mode)
        ## La información que retorna solo es de la posición colocada más no de la posición abierta
        market_order_params = {
            'quantity' : '14',
            'symbol' : symbol
        }

        # Probando Ordnes Market - OK
        #resp = await exchange.create_buy_market_order(params=market_order_params)
        #print(resp)
        #resp = await exchange.create_sell_market_order(params=market_order_params)
        #print(resp)

        # Probando Ordenes Limit

        print("Fin")

    except Exception as e:
        print(e)
    finally:
        await exchange.close_connection()


if __name__ == '__main__':
    asyncio.run(main())
