import logging

from pybit import exceptions
from pybit.unified_trading import HTTP

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

API_KEY = 'dqk8oFrkLOA7vFEy6N'
SECRET_KEY = 'ghtWTidrREYAaOaZMUb3Sp4CIrkfNagRBm6N'


def main():
    client = HTTP(
        recv_window=60000,
        testnet=True,
        api_key=API_KEY,
        api_secret=SECRET_KEY
    )

    try:
        r = client.place_order(
            category='spot',
            symbol='SOLUSDT',
            side='BUY',
            orderType='Market',
            qty=5
        )
        print(r)
    except exceptions.InvalidRequestError as e:
        print(e.status_code, e.message, sep=' | ')
    except exceptions.FailedRequestError as e:
        print("Request failed. Error:", e.status_code, e.message)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
