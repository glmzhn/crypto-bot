from client import TVCSClient
from place_order import buy_or_sell
import json


def get_signal():

    client = TVCSClient()

    pairs = ["BTCUSDT"]

    exchange = "BINANCE"
    interval = "1h"

    signals = []

    for pair in pairs:
        signal = client.get_signal(symbol=pair, exchange=exchange, interval=interval)
        signals.append(signal)
        with open('signals.json', 'w') as f:
            json.dump(signals, f, indent=4)

        buy_or_sell(
            category='spot',
            symbol=signal['pair'],
            side=signal['recommendation'].lower(),
            ordertype='Market',
            qty=1
        )


if __name__ == "__main__":
    get_signal()
