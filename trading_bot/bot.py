# Python
import asyncio
from decimal import Decimal
# Project
from exchanges.binance import Binance
from models.asset import Asset
from data import info
from abstracts.strategy import Strategy
from strategies.larry_connors_mod_one import LarryConnorsModOneStrategy
# Third party
from decouple import config
import binance.enums as tf
from utils.telegram_notifier import TelegramNotifier

async def process_message(msg: dict):
    print(msg)


async def main():
    
    # 1. Solicitar symbol
    symbol = "MATICUSDT"
    asset = Asset(symbol=symbol)

    # 2. En teoría, con el AssetDao extraemos la información de la moneda pero ahorita no tememos
    #    la BD para extraer y tabién Creamos un OrderDao que guardará los datos de órdenes en BD
    #    El OrderDao será inyectado a la estrategia
    asset.price_precision = info[symbol.lower()]["price_precision"]
    asset.qty_precision = info[symbol.lower()]["qty_precision"]
    asset.min_price = info[symbol.lower()]["min_price"]
    asset.min_qty = info[symbol.lower()]["min_qty"]

    try:
        # 3. Creando Exchange
        exchange = Binance(api_key=config("API_KEY"), api_secret=config("API_SECRET"))

        # 4. Notifier que tendra el método de clase enviar mensaje pero será usado directamente en la
        #    Estrategia
        
        # 5. Solicitamos y creamos la estrategia. La estraegía recibirá el exchange para poder ejecutar lo que
        #    necesite de este; también necesita que se le inyecte el asset para poder usar los datos de la moneda
        #    Con el Notifier creado, también se le inyectará para que sea a través de este quien notifique al
        #    medio deseado
        strategy = LarryConnorsModOneStrategy(asset=asset, exchange=exchange)
        await strategy.start()

       
        print("Fin")

    except Exception as e:
        print(e)
    finally:
        await exchange.close_connection()

    
if __name__ == '__main__':
    asyncio.run(main())
