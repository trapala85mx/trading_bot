# Summary

This is a script to create a trading bot that will open and close positions into the Exchange according to the strategy selected


# Pre requisistes
- Python 3.10
- Ta Lib Wheel Installed.<br>You can go either https://trapalamx.notion.site/Ta-Lib-b048ef6dfddc454cb579fbccc1e6a1cb?pvs=4 or https://github.com/ta-lib/ta-lib-python to check how to install in Linux / WSL2. For windows install check the github page
- Create an API in Binance (api key and api secret needed)
- Create you bot from Telegram for signals (telegram token and telegram chat id needed)

# Execute (Linux / Wsl2)
1. Clone repo
```shell
# SSH
git clone git@github.com:trapala85mx/trading_bot.git
# HTTPS
git clone https://github.com/trapala85mx/trading_bot.git
```

2. Move to folder
```shell
cd trading_bot
```
3. Create a .env file
```shell
touch .env
```

4. Fill the .env file with theese data:
```
[BINANCE]
API_KEY = "your api key from binance"
API_SECRET = "your api secret from binance"

[TELEGRAM]
TELEGRAM_TOKEN = "your telegram token"
TELEGRAM_CHAT_ID = "your chat id fro mtelegram"
```
5. Create virtual environment of Python 3.10

6. Activate virtual environment

7. Install requirements.txt
```shell
pip install -r requirements.txt
```

8. Go to trading_bot/data.py and fille the info with the cryptos to trade. i´m working on this to not do this.<br>
In this file you need to add precisions and minimun qtys/price

9. Executing. To trade the crypto you want, go to line 22 in the trading_bot/bot.py and change it (im working in this to not do this). After this, execute from root folder:
```shell
python trading_bot/bot.py
```


# Notes
For now just 1 strategy is implemented (Larry Connors)


# TO DO
- Get all crypto info from Database (working in it in crypto_info repo)
- Search for crypto with more volume to trade just theese ones
- Modify creating orders functions from params to specific variables
- Implement Bybit Exchange
- Implement Bingx Exchange