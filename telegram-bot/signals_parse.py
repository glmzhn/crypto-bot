import datetime

from aiogram.types import Message
from pybit import exceptions
from pybit.unified_trading import HTTP

from client import TVCSClient
import json
from place_order import check_balance

# | API Keys |
API_KEY = 'dqk8oFrkLOA7vFEy6N'
SECRET_KEY = 'ghtWTidrREYAaOaZMUb3Sp4CIrkfNagRBm6N'

# | Connecting to the API |
app = HTTP(
        recv_window=60000,
        testnet=True,
        api_key=API_KEY,
        api_secret=SECRET_KEY
    )


async def get_signal(message: Message):

    client = TVCSClient()

    pairs = ["BTCUSDT"]

    exchange = "BINANCE"
    interval = "1h"

    signals = []

    for pair in pairs:
        signal = client.get_signal(symbol=pair, exchange=exchange, interval=interval)
        signals.append(signal)
        with open('../outcome_data/signals.json', 'w') as f:
            json.dump(signals, f, indent=4)

        try:
            if signal['recommendation'] == 'STRONG_BUY':
                r = app.place_order(
                    category='linear',
                    symbol=signal['pair'],
                    side='Buy',
                    orderType='Market',
                    qty=0.001,
                    marketunit='quoteCoin'
                )

                print(r)

                if r['retMsg'] == 'OK':
                    time = r['time'] / 1000
                    dt_object = datetime.datetime.fromtimestamp(time)
                    await message.answer(f"Покупка успешно произведена! \U00002705\n"
                                         f"ID Ордера: {r['result']['orderId']} \U0001F4DD\n"
                                         f"Время: {dt_object} \U0000231A")
                else:
                    await message.answer('Покупка не была произведена, произошла ошибка \U0000274C')

            elif signal['recommendation'] == 'STRONG_SELL':
                with open('account.txt', 'r', encoding='utf-8') as f:
                    account = f.read().strip()
                totalwalletbalance, coin_type, availablebalance = check_balance(account)

                if totalwalletbalance == availablebalance:
                    print('Нет доступных монет для покупки')
                else:
                    r = app.place_order(
                        category='linear',
                        symbol=signal['pair'],
                        side='Sell',
                        orderType='Market',
                        qty=0.001,
                        marketunit='quoteCoin'
                    )

                    if r['retMsg'] == 'OK':
                        time = r['time'] / 1000
                        dt_object = datetime.datetime.fromtimestamp(time)
                        await message.answer(f"Продажа успешно произведена! \U00002705\n"
                                             f"ID Ордера: {r['result']['orderId']} \U0001F4DD\n"
                                             f"Время: {dt_object} \U0000231A")
                    else:
                        await message.answer('Продажа не была произведена, произошла ошибка \U0000274C')

            elif signal['recommendation'] == 'NEUTRAL':
                print('Recommendation was neutral')
                await message.answer('Рекомендация была нейтральной, покупка не производится \U000026D4')

            elif signal['recommendation'] == 'BUY':
                r = app.place_order(
                    category='linear',
                    symbol=signal['pair'],
                    side='Buy',
                    orderType='Market',
                    qty=0.001,
                    marketunit='quoteCoin'
                )

                print(r)

                if r['retMsg'] == 'OK':
                    time = r['time'] / 1000
                    dt_object = datetime.datetime.fromtimestamp(time)
                    await message.answer(f"Покупка успешно произведена! \U00002705\n"
                                         f"ID Ордера: {r['result']['orderId']} \U0001F4DD\n"
                                         f"Время: {dt_object} \U0000231A")
                else:
                    await message.answer('Покупка не была произведена, произошла ошибка \U0000274C')

            elif signal['recommendation'] == 'SELL':
                with open('account.txt', 'r', encoding='utf-8') as f:
                    account = f.read().strip()
                totalwalletbalance, coin_type, availablebalance = check_balance(account)
                if totalwalletbalance == availablebalance:
                    print('Нет доступных монет для покупки')
                else:
                    r = app.place_order(
                        category='linear',
                        symbol=signal['pair'],
                        side='Sell',
                        orderType='Market',
                        qty=0.001,
                        marketunit='quoteCoin'
                    )

                    if r['retMsg'] == 'OK':
                        time = r['time'] / 1000
                        dt_object = datetime.datetime.fromtimestamp(time)
                        await message.answer(f"Продажа успешно произведена! \U00002705\n"
                                             f"ID Ордера: {r['result']['orderId']} \U0001F4DD\n"
                                             f"Время: {dt_object} \U0000231A")
                    else:
                        await message.answer('Продажа не была произведена, произошла ошибка \U0000274C')

        # | Exceptions messages |
        except exceptions.InvalidRequestError as e:
            print(e.status_code, e.message, sep=' | ')
            if e.status_code == 110007:
                await message.answer('Недостаточно свободных средств для покупки! \U0000274C\U0001F4B0')
        except exceptions.FailedRequestError as e:
            print("Request failed. Error:", e.status_code, e.message)
        except Exception as e:
            print(e)
