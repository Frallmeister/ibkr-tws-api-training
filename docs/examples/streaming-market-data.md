# Streaming market data example

Runnable file:

```text
examples/03_market_data/streaming_market_data.py
```

This example introduces two things at once:

- a long-lived `reqMktData()` subscription;
- running `app.run()` on a background thread so the main thread remains available.

## Run it

Start TWS in paper trading, then from the repository root run:

```powershell
uv run python examples/03_market_data/streaming_market_data.py
```

The script subscribes to NVDA for ten seconds, cancels the subscription, disconnects, and waits for the API thread to finish.

## Complete example

```python
from decimal import Decimal
from threading import Event, Thread
from time import sleep

from ibapi.client import EClient
from ibapi.common import TickAttrib
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
from ibapi.wrapper import EWrapper

REQUEST_ID = 2
STREAM_SECONDS = 10


def create_stock_contract() -> Contract:
    contract = Contract()
    contract.symbol = "NVDA"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "NASDAQ"
    return contract


class StreamingMarketDataApp(EWrapper, EClient):
    def __init__(self) -> None:
        EClient.__init__(self, wrapper=self)
        self.subscription_started = Event()

    def nextValidId(self, orderId: int) -> None:
        print(f"Connected. Next valid order ID: {orderId}")
        self.reqMktData(
            reqId=REQUEST_ID,
            contract=create_stock_contract(),
            genericTickList="",
            snapshot=False,
            regulatorySnapshot=False,
            mktDataOptions=[],
        )
        self.subscription_started.set()

    def tickPrice(
        self,
        reqId: int,
        tickType: int,
        price: float,
        attrib: TickAttrib,
    ) -> None:
        tick_name = TickTypeEnum.toStr(tickType)
        print(f"PRICE  reqId={reqId}  {tick_name}={price}")

    def tickSize(self, reqId: int, tickType: int, size: Decimal) -> None:
        tick_name = TickTypeEnum.toStr(tickType)
        print(f"SIZE   reqId={reqId}  {tick_name}={size}")


def main() -> None:
    app = StreamingMarketDataApp()
    app.connect(host="127.0.0.1", port=7497, clientId=1)

    api_thread = Thread(target=app.run, name="ibkr-api")
    api_thread.start()

    if not app.subscription_started.wait(timeout=5):
        app.disconnect()
        api_thread.join()
        raise RuntimeError("Market-data subscription did not start")

    sleep(STREAM_SECONDS)

    app.cancelMktData(REQUEST_ID)
    app.disconnect()
    api_thread.join()


if __name__ == "__main__":
    main()
```

## Follow the execution

The main thread first connects to TWS and starts another Python thread whose target is:

```python
app.run
```

That API thread remains inside the TWS message-processing loop and dispatches `EWrapper` callbacks.

When `nextValidId()` arrives, the callback starts the subscription and sets a `threading.Event`. The main thread is waiting for that event, so it does not rely on a guessed startup delay.

After ten seconds the main thread calls:

```python
app.cancelMktData(REQUEST_ID)
```

then disconnects and calls:

```python
api_thread.join()
```

`join()` waits for the API thread to finish before the process exits.

## What to observe

The same `reqId=2` appears on all callbacks belonging to this subscription, while the tick type changes according to the data being updated.

Try changing `STREAM_SECONDS` first. Then compare `snapshot=False` with the snapshot behavior documented by IBKR. Leave generic tick types for the next chapter, where the different tick fields are introduced systematically.
