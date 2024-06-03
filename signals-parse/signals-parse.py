import json

from client import TVCSClient


def main():

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


if __name__ == "__main__":
    main()
