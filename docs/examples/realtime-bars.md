# Real-time bars example

Runnable file:

```text
examples/03_market_data/realtime_bars.py
```

This example adds one new market-data abstraction:

- a long-lived `reqRealTimeBars()` subscription that emits completed 5-second bars.

It deliberately reuses the same threading and shutdown pattern introduced by the streaming-market-data example.

## Run it

Start TWS in paper trading, then from the repository root run:

```powershell
uv run python examples/03_market_data/realtime_bars.py
```

The script subscribes to NVDA for twenty seconds, cancels the subscription, disconnects, and waits for the API thread to finish.

## Complete example

```python
from decimal import Decimal
from threading import Event, Thread
from time import sleep

from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper

REQUEST_ID = 3
STREAM_SECONDS = 20


def create_stock_contract() -> Contract:
    contract = Contract()
    contract.symbol = "NVDA"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "NASDAQ"
    return contract


class RealTimeBarsApp(EWrapper, EClient):
    def __init__(self) -> None:
        EClient.__init__(self, wrapper=self)
        self.subscription_started = Event()

    def nextValidId(self, orderId: int) -> None:
        print(f"Connected. Next valid order ID: {orderId}")
        self.reqRealTimeBars(
            reqId=REQUEST_ID,
            contract=create_stock_contract(),
            barSize=5,
            whatToShow="TRADES",
            useRTH=True,
            realTimeBarsOptions=[],
        )
        self.subscription_started.set()

    def realtimeBar(
        self,
        reqId: int,
        time: int,
        open_: float,
        high: float,
        low: float,
        close: float,
        volume: Decimal,
        wap: Decimal,
        count: int,
    ) -> None:
        print(
            f"BAR reqId={reqId} time={time} "
            f"open={open_} high={high} low={low} close={close} "
            f"volume={volume} wap={wap} count={count}"
        )


def main() -> None:
    app = RealTimeBarsApp()
    app.connect(host="127.0.0.1", port=7497, clientId=1)

    api_thread = Thread(target=app.run, name="ibkr-api")
    api_thread.start()

    if not app.subscription_started.wait(timeout=5):
        app.disconnect()
        api_thread.join()
        raise RuntimeError("Real-time-bar subscription did not start")

    sleep(STREAM_SECONDS)

    app.cancelRealTimeBars(REQUEST_ID)
    app.disconnect()
    api_thread.join()


if __name__ == "__main__":
    main()
```

## Follow the execution

The connection and background API thread work exactly as in the previous streaming example.

Once `nextValidId()` confirms readiness, the application starts:

```python
self.reqRealTimeBars(...)
```

IBKR then invokes `realtimeBar()` once for each completed 5-second bar. All bars from this subscription carry the same `reqId=3`.

After twenty seconds the main thread stops the stream with:

```python
app.cancelRealTimeBars(REQUEST_ID)
```

and then shuts down the connection cleanly.

## What to observe

Focus on how the callback differs from `tickPrice()` and `tickSize()`:

- one `realtimeBar()` callback contains the bar's OHLC values together;
- successive callbacks represent successive 5-second intervals;
- the request remains active until it is explicitly cancelled;
- `reqId=3` correlates every returned bar with the original subscription.

Try changing `useRTH` only after the basic example works. Keep `barSize=5`; `reqRealTimeBars()` is the fixed 5-second bar interface.
