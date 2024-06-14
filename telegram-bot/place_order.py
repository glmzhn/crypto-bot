import logging
import os

from dotenv import load_dotenv
from pybit import exceptions
from pybit.unified_trading import HTTP
from aiogram.types import Message

# | Logging |
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

load_dotenv()

# | API Keys |
API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('API_SECRET')

# | Connecting to the API |
client = HTTP(
        recv_window=60000,
        testnet=True,
        api_key=API_KEY,
        api_secret=SECRET_KEY
    )


# | Function to place the order for buying or selling |
def buy_or_sell(category, symbol, side, ordertype, qty, marketunit):
    try:
        balance = client.place_order(
            category=category,  # | One of them: linear, inverse, option, spot |
            symbol=symbol,  # | Example: BTCUSDT, SOLUSDT, ETHUSDT |
            side=side,  # | Buy or Sell |
            orderType=ordertype,  # | One of them: Market, Limit |
            qty=qty,  # | Count of coins |
            marketUnit=marketunit
        )
        return balance
    # | Exceptions messages |
    except exceptions.InvalidRequestError as e:
        print(e.status_code, e.message, sep=' | ')
    except exceptions.FailedRequestError as e:
        print("Request failed. Error:", e.status_code, e.message)
    except Exception as e:
        print(e)


# | Function to check balance of the wallet |
def check_balance(accounttype):
    try:
        # | accountType can be one of them: UNIFIED, CONTRACT, SPOT |
        balance = client.get_wallet_balance(accountType=accounttype)
        totalavailablebalance = balance['result']['list'][0]['totalAvailableBalance']
        amount = balance['result']['list'][0]['totalWalletBalance']
        return amount, totalavailablebalance
    # | Exceptions messages |
    except exceptions.InvalidRequestError as e:
        print(e.status_code, e.message, sep=' | ')
    except exceptions.FailedRequestError as e:
        print("Request failed. Error:", e.status_code, e.message)
    except Exception as e:
        print(e)


# | Function to cancel orders |
async def cancel_order(category, symbol, orderid, message: Message):
    try:
        c = client.cancel_order(
            category=category,  # | One of them: linear, inverse, option, spot |
            symbol=symbol,  # | Example: BTCUSDT, SOLUSDT, ETHUSDT |
            orderId=orderid,  # | Order's id |
        )
        return c
    # | Exceptions messages |
    except exceptions.InvalidRequestError as e:
        print(e.status_code, e.message, sep=' | ')
        if e.status_code == 110001:
            await message.answer('Неверный id ордера, либо ордер уже исполнен и отмена невозможна')
    except exceptions.FailedRequestError as e:
        print("Request failed. Error:", e.status_code, e.message)
    except Exception as e:
        print(e)


# | Function to get all orders or a certain order |
def get_orders(category, symbol, orderid=None):
    try:
        if orderid is None:
            c = client.get_open_orders(
                category=category,  # | One of them: linear, inverse, option, spot |
                symbol=symbol,  # | Example: BTCUSDT, SOLUSDT, ETHUSDT |
                openOnly=2,  # | 0 - Only active orders, 1 - Orders with final status, 2 - All orders
            )
            return c
        else:
            c = client.get_open_orders(
                category=category,  # | One of them: linear, inverse, option, spot |
                symbol=symbol,  # | Example: BTCUSDT, SOLUSDT, ETHUSDT |
                orderId=orderid,  # | Order's id |
                openOnly=2,  # | 0 - Only active orders, 1 - Orders with final status, 2 - All orders
            )
            return c
    # | Exceptions messages |
    except exceptions.InvalidRequestError as e:
        print(e.status_code, e.message, sep=' | ')
    except exceptions.FailedRequestError as e:
        print("Request failed. Error:", e.status_code, e.message)
    except Exception as e:
        print(e)
