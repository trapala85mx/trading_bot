# Python
import asyncio
from decimal import Decimal
# Project
from exchanges.binance import Binance
from models.asset import Asset
from data import info
# Third party
from decouple import config
import binance.enums as tf


async def process_message(msg: dict):
    print(msg)


async def main():
    print("Hola")
    # 1. Solicitar symbol
    symbol = "MANAUSDT"
    print("Creando Asset")
    asset = Asset(symbol=symbol)

    # 2. En teoría, con el AssetDao extraemos la información de la moneda pero ahorita no tememos
    #    la BD para extraer y tabién Creamos un OrderDao que guardará los datos de órdenes en BD
    #    El OrderDao será inyectado a la estrategia
    asset.price_precision = info[symbol.lower()]["price_precision"]
    asset.qty_precision = info[symbol.lower()]["qty_precision"]
    asset.min_price = info[symbol.lower()]["min_price"]
    asset.min_qty = info[symbol.lower()]["min_qty"]
    print("Asset Creado")

    # 3. Creando Exchange
    exchange = Binance(api_key=config("API_KEY"), api_secret=config("API_SECRET"))

    # 4. Crear Notifier. Por el momento lo omitimos

    # 5. Solicitamos y creamos la estrategia. La estraegía recibirá el exchange para poder ejecutar lo que
    #    necesite de este; el order_dao será inyectado para poder guardar datos de órdenes creadas. Por otra
    #    parte, la estrategia creará las Ordenes necesarias, es decir, crear instnacias de Order y también
    #    necesitará que le inyecten el objeto asset para poder obtener datos particulares de la moneda


    # 2. Solicitar Exchange a usar
    # Por el momento solo tenemos 1 estrategua y 1 exchange por lo que omitimos lo anterior

    # Creamos el objeto Exchange que será algo abstracto para que se iguale a lo que ingrese el usuario

    # Datos para ejemplo
    interval = tf.KLINE_INTERVAL_15MINUTE
    
    try:
        # data = await exchange.get_klines(interval=interval, symbol=symbol)
        # data = await exchange.get_exchange_info() # sin symbol
        # data = await exchange.get_exchange_info(symbol=symbol)  # conn symbol
        # print(data)
        # await exchange.kline_socket(symbol=symbol, timeframe=interval, callback=process_message)
        #await exchange.user_socket(callback=process_message)

        # Probando extraer Exchange Mode - OK
        #await exchange.get_current_position_mode()
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

        # Probando Ordenes Limit - OK

        #buy_limit_order_params = {
        #    'symbol': 'BTCUSDT',
        #    'entry_price': Decimal('28966'),
        #    'quantity': Decimal('0.001')
        #}
        #resp = await exchange.create_buy_limit_order(params=buy_limit_order_params)
        #print(resp)

        #sell_limit_order_params = {
        #    'symbol': 'BTCUSDT',
        #    'entry_price': Decimal('29226.4'),
        #    'quantity': Decimal('0.001')
        #}
        #resp = await exchange.create_sell_limit_order(params=sell_limit_order_params)
        #print(resp)

        # PRoBANDO ORDENES STOP LOSS - OK
        #sl_for_shorts_param = {
        #    'symbol': 'BTCUSDT',
        #    'stop_loss_price': Decimal('29484.5'), # Para posicion corta
        #    'stop_loss_price': Decimal('29035.5'), # para posicion larga
        #}
        ##resp = await exchange.set_stop_loss_for_short_position(params=sl_for_shorts_param)
        #resp = await exchange.set_stop_loss_for_long_position(params=sl_for_shorts_param)
        #print(resp)

        # ORDENES TP LIMIT - OK
        #take_profit_for_short_pos_params = {
        #    'symbol': "BTCUSDT",
        #    'quantity': Decimal('0.002'),
        #    'stop_loss_price': Decimal('29001.5')
        #}
        #resp = await exchange.set_take_profit_for_short_position_in_hedge_mode(params=take_profit_for_short_pos_params)
        #print(resp)
        print("Fin")

    except Exception as e:
        print(e)
    finally:
        await exchange.close_connection()


if __name__ == '__main__':
    asyncio.run(main())
