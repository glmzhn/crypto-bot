import json
import logging

from pybit import exceptions
from pybit.unified_trading import HTTP

# | Logging |
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

# | API Keys |
API_KEY = 'dqk8oFrkLOA7vFEy6N'
SECRET_KEY = 'ghtWTidrREYAaOaZMUb3Sp4CIrkfNagRBm6N'

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
        with open('../outcome_data/wallet.json', 'w') as f:
            json.dump(balance, f, indent=4)
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


def cancel_order(category, symbol, orderid):
    try:
        c = client.cancel_order(
            category=category,  # | One of them: linear, inverse, option, spot |
            symbol=symbol,  # | Example: BTCUSDT, SOLUSDT, ETHUSDT |
            orderid=orderid,  # | Order's id |
        )
        return c
    # | Exceptions messages |
    except exceptions.InvalidRequestError as e:
        print(e.status_code, e.message, sep=' | ')
    except exceptions.FailedRequestError as e:
        print("Request failed. Error:", e.status_code, e.message)
    except Exception as e:
        print(e)


def get_orders(category, symbol, orderid=None):
    try:
        if orderid is None:
            c = client.get_open_orders(
                category=category,  # | One of them: linear, inverse, option, spot |
                symbol=symbol,
                openOnly=2,
            )
            with open('../outcome_data/order.json', 'w') as f:
                json.dump(c, f, indent=4)
            return c
        else:
            c = client.get_open_orders(
                category=category,  # | One of them: linear, inverse, option, spot |
                symbol=symbol,
                orderId=orderid,
                openOnly=2,
            )
            with open('../outcome_data/order.json', 'w') as f:
                json.dump(c, f, indent=4)
            return c
    # | Exceptions messages |
    except exceptions.InvalidRequestError as e:
        print(e.status_code, e.message, sep=' | ')
    except exceptions.FailedRequestError as e:
        print("Request failed. Error:", e.status_code, e.message)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # get_single_order('linear', 'BTCUSDT')
    cancel_order('linear', 'BTCUSDT', '6ce2a705-a215-41b0-b758-48b31ce30216')
