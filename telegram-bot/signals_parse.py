from aiogram.types import Message

from client import TVCSClient
from place_order import buy_or_sell
import json


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

        if signal['recommendation'] == 'STRONG_BUY':
            r = buy_or_sell(
                category='linear',
                symbol=signal['pair'],
                side='Buy',
                ordertype='Market',
                qty=0.01,
                marketunit='quoteCoin'
            )

            if r['retMsg'] == 'OK':
                await message.answer(f"Покупка успешно произведена! \U00002705\n"
                                     f"ID Ордера: {r['result']['orderId']} \U0001F4DD\n"
                                     f"Время: {r['time']} \U0000231A")
            elif r['retMsg'] == 'None':
                await message.answer('Покупка не была произведена, произошла ошибка \U0000274C')

        elif signal['recommendation'] == 'STRONG_SELL':
            r = buy_or_sell(
                category='linear',
                symbol=signal['pair'],
                side='Sell',
                ordertype='Market',
                qty=0.01,
                marketunit='quoteCoin'
            )

            print(r)

            if r['retMsg'] == 'OK':
                await message.answer(f"Продажа успешно произведена! \U00002705\n"
                                     f"ID Ордера: {r['result']['orderId']} \U0001F4DD\n"
                                     f"Время: {r['time']} \U0000231A")
            elif r['retMsg'] == 'None':
                await message.answer('Продажа не была произведена, произошла ошибка \U0000274C')

        elif signal['recommendation'] == 'NEUTRAL':
            print('Recommendation was neutral')
            await message.answer('Рекомендация была нейтральной, покупка не производится \U000026D4')

        elif signal['recommendation'] == 'BUY':
            r = buy_or_sell(
                category='linear',
                symbol=signal['pair'],
                side='Buy',
                ordertype='Market',
                qty=0.01,
                marketunit='quoteCoin'
            )

            print(r)

            if r['retMsg'] == 'OK':
                await message.answer(f"Покупка успешно произведена! \U00002705\n"
                                     f"ID Ордера: {r['result']['orderId']} \U0001F4DD\n"
                                     f"Время: {r['time']} \U0000231A")
            elif r['retMsg'] == 'None':
                await message.answer('Покупка не была произведена, произошла ошибка \U0000274C')

        elif signal['recommendation'] == 'SELL':
            r = buy_or_sell(
                category='linear',
                symbol=signal['pair'],
                side='Sell',
                ordertype='Market',
                qty=0.01,
                marketunit='quoteCoin'
            )

            print(r)

            if r['retMsg'] == 'OK':
                await message.answer(f"Продажа успешно произведена! \U00002705\n"
                                     f"ID Ордера: {r['result']['orderId']} \U0001F4DD\n"
                                     f"Время: {r['time']} \U0000231A")
            elif r['retMsg'] == 'None':
                await message.answer('Продажа не была произведена, произошла ошибка \U0000274C')

