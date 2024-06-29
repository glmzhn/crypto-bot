import datetime
import os
import sqlite3
from aiogram import Bot
from pybit import exceptions
from pybit.unified_trading import HTTP
from place_order import get_orders
from client import TVCSClient
from place_order import check_balance
from dotenv import load_dotenv


load_dotenv()

# | API Keys |
API_KEY = os.environ['API_KEY']
SECRET_KEY = os.environ['API_SECRET']

# | Connecting to the API |
app = HTTP(
        recv_window=60000,
        api_key=API_KEY,
        api_secret=SECRET_KEY,
        testnet=True
    )


conn = sqlite3.connect('accounts.db')

cur = conn.cursor()


async def get_signal(bot: Bot):
    user_id = '962394481'
    cur.execute("SELECT account, qty FROM user_account WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    account = result[0]
    qty = result[1]

    client = TVCSClient()

    pairs = ["BTCUSDT"]

    exchange = "BINANCE"
    interval = "1h"

    for pair in pairs:
        signal = client.get_signal(symbol=pair, exchange=exchange, interval=interval)

        try:
            if signal['recommendation'] == 'STRONG_BUY':
                r = app.place_order(
                    category='linear',
                    symbol=signal['pair'],
                    side='Buy',
                    orderType='Market',
                    qty=qty,
                    marketunit='quoteCoin'
                )

                print(r)

                if r['retMsg'] == 'OK':
                    time = r['time'] / 1000
                    dt_object = datetime.datetime.fromtimestamp(time)
                    order_status = get_orders('linear', 'BTCUSDT', orderid=r['result']['orderId'])
                    if order_status['result']['list']['orderStatus'] == 'Filled':
                        await bot.send_message(text=f"Покупка успешно произведена! \U00002705\n"
                                               f"ID Ордера: {r['result']['orderId']} \U0001F4DD\n"
                                               f"Время: {dt_object} \U0001F550\n"
                                               f"Статус заказа: Исполнен \U0001F4E8", chat_id=user_id)
                else:
                    await bot.send_message(text='Покупка не была произведена, '
                                                'произошла ошибка \U0000274C', chat_id=user_id)

            elif signal['recommendation'] == 'STRONG_SELL':

                totalwalletbalance, availablebalance = check_balance(account)

                if totalwalletbalance == availablebalance:
                    await bot.send_message(text='Нет доступных монет для продажи \U0000274C\U0001F4B0', chat_id=user_id)
                else:
                    r = app.place_order(
                        category='linear',
                        symbol=signal['pair'],
                        side='Sell',
                        orderType='Market',
                        qty=qty,
                        marketunit='quoteCoin'
                    )

                    if r['retMsg'] == 'OK':
                        time = r['time'] / 1000
                        dt_object = datetime.datetime.fromtimestamp(time)
                        order_status = get_orders('linear', 'BTCUSDT', orderid=r['result']['orderId'])
                        if order_status['result']['list']['orderStatus'] == 'Filled':
                            await bot.send_message(text=f"Продажа успешно произведена! \U00002705\n"
                                                   f"ID Ордера: {r['result']['orderId']} \U0001F4DD\n"
                                                   f"Время: {dt_object} \U0001F550\n"
                                                   f"Статус заказа: Исполнен \U0001F4E8", chat_id=user_id)
                    else:
                        await bot.send_message(text='Продажа не была произведена, '
                                                    'произошла ошибка \U0000274C', chat_id=user_id)

            elif signal['recommendation'] == 'NEUTRAL':
                await bot.send_message(text='Рекомендация была нейтральной, '
                                            'покупка не производится \U000026D4', chat_id=user_id)

            elif signal['recommendation'] == 'BUY':
                r = app.place_order(
                    category='linear',
                    symbol=signal['pair'],
                    side='Buy',
                    orderType='Market',
                    qty=qty,
                    marketunit='quoteCoin'
                )

                print(r)

                if r['retMsg'] == 'OK':
                    time = r['time'] / 1000
                    dt_object = datetime.datetime.fromtimestamp(time)
                    order_status = get_orders('linear', 'BTCUSDT', orderid=r['result']['orderId'])
                    if order_status['result']['list']['orderStatus'] == 'Filled':
                        await bot.send_message(text=f"Покупка успешно произведена! \U00002705\n"
                                               f"ID Ордера: {r['result']['orderId']} \U0001F4DD\n"
                                               f"Время: {dt_object} \U0001F550\n"
                                               f"Статус заказа: Исполнен \U0001F4E8", chat_id=user_id)
                else:
                    await bot.send_message(text='Покупка не была произведена, '
                                                'произошла ошибка \U0000274C', chat_id=user_id)

            elif signal['recommendation'] == 'SELL':
                totalwalletbalance, availablebalance = check_balance(account)
                if totalwalletbalance == availablebalance:
                    await bot.send_message(text='Нет доступных монет для продажи \U0000274C\U0001F4B0', chat_id=user_id)
                else:
                    r = app.place_order(
                        category='linear',
                        symbol=signal['pair'],
                        side='Sell',
                        orderType='Market',
                        qty=qty,
                        marketunit='quoteCoin'
                    )

                    if r['retMsg'] == 'OK':
                        time = r['time'] / 1000
                        dt_object = datetime.datetime.fromtimestamp(time)
                        order_status = get_orders('linear', 'BTCUSDT', orderid=r['result']['orderId'])
                        if order_status['result']['list']['orderStatus'] == 'Filled':
                            await bot.send_message(text=f"Продажа успешно произведена! \U00002705\n"
                                                   f"ID Ордера: {r['result']['orderId']} \U0001F4DD\n"
                                                   f"Время: {dt_object} \U0001F550\n"
                                                   f"Статус заказа: Исполнен \U0001F4E8", chat_id=user_id)
                    else:
                        await bot.send_message(text='Продажа не была произведена, '
                                                    'произошла ошибка \U0000274C', chat_id=user_id)

        # | Exceptions messages |
        except exceptions.InvalidRequestError as e:
            print(e.status_code, e.message, sep=' | ')
            if e.status_code == 110007:
                await bot.send_message(text='Недостаточно свободных '
                                            'средств для покупки! \U0000274C\U0001F4B0', chat_id=user_id)
        except exceptions.FailedRequestError as e:
            print("Request failed. Error:", e.status_code, e.message)
        except Exception as e:
            print(e)
