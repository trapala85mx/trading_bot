import requests
from decouple import config
import asyncio
from abstracts.notifier import Notifier

class TelegramNotifier(Notifier):
    """Class that send signal to Telegram
    """    
    
    @classmethod
    async def send_message(cls, msg: str):
        
        url = f"https://api.telegram.org/bot{config('TELEGRAM_TOKEN')}/sendMessage"
        data = {"chat_id": config('TELEGRAM_CHAT_ID'), "text": msg}
        
        response = requests.post(url, data=data)
        
        return response
