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
def buy_or_sell(category, symbol, side, ordertype, qty):
    try:
        r = client.place_order(
            category=category,  # | One of them: linear, inverse, option, spot |
            symbol=symbol,  # | Example: BTCUSDT, SOLUSDT, ETHUSDT |
            side=side,  # | Buy or Sell |
            orderType=ordertype,  # | One of them: Market, Limit |
            qty=qty,  # | Count of coins |
        )
        print(r)
    # | Exceptions messages |
    except exceptions.InvalidRequestError as e:
        print(e.status_code, e.message, sep=' | ')
    except exceptions.FailedRequestError as e:
        print("Request failed. Error:", e.status_code, e.message)
    except Exception as e:
        print(e)
