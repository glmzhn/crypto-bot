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
        with open('../signals-parse/signals.json', 'w') as f:
            json.dump(signals, f, indent=4)

        if signal['recommendation'] == 'STRONG_BUY':
            signal['recommendation'] = 'BUY'

        elif signal['recommendation'] == 'STRONG_SELL':
            signal['recommendation'] = 'SELL'

            buy_or_sell(
                category='spot',
                symbol=signal['pair'],
                side=signal['recommendation'],
                ordertype='Market',
                qty=0.000000001
            )
            print(signal['recommendation'])


if __name__ == "__main__":
    get_signal()
