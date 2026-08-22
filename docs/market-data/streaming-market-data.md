# Streaming market data

Historical data is a finite request: IBKR sends a set of bars and then calls an end callback.

Streaming market data is different. `reqMktData()` opens a subscription that stays active until you cancel it.

The runnable example is:

```text
examples/03_market_data/streaming_market_data.py
```

It subscribes to NVDA for ten seconds and then cancels the subscription.

## The subscription

The request is:

```python
self.reqMktData(
    reqId=REQUEST_ID,
    contract=create_stock_contract(),
    genericTickList="",
    snapshot=False,
    regulatorySnapshot=False,
    mktDataOptions=[],
)
```

For this first example, the important parameters are:

| Parameter | Meaning |
| --- | --- |
| `reqId` | Identifies this subscription in later callbacks |
| `contract` | Instrument to subscribe to |
| `genericTickList=""` | Request only the standard market-data fields |
| `snapshot=False` | Keep streaming instead of returning a one-time snapshot |
| `regulatorySnapshot=False` | Do not request a paid regulatory snapshot |

The request does not return a quote object. Updates arrive asynchronously through `EWrapper` callbacks.

## What comes back?

IBKR documents `tickPrice()` and `tickSize()` as the main callbacks for a standard `reqMktData()` request.

```python
from ibapi.ticktype import TickTypeEnum


def tickPrice(self, reqId, tickType, price, attrib):
    print(reqId, TickTypeEnum.toStr(tickType), price)


def tickSize(self, reqId, tickType, size):
    print(reqId, TickTypeEnum.toStr(tickType), size)
```

A single subscription can therefore generate many callbacks of different tick types:

```text
BID
ASK
LAST
BID_SIZE
ASK_SIZE
LAST_SIZE
...
```

The next chapter studies tick types in detail. For now, the important point is that `reqId` tells you which subscription produced an update, while `tickType` tells you what kind of update it is.

## There is no `marketDataEnd()` callback

This subscription has no natural completion point.

The lifecycle is:

```text
reqMktData(2, ...)
        ↓
tickPrice(2, ...)
tickSize(2, ...)
tickPrice(2, ...)
...
        ↓
cancelMktData(2)
```

You stop the stream explicitly with the same request ID:

```python
self.cancelMktData(REQUEST_ID)
```

This is how you can recognize the pattern in the IBKR documentation as well: the request documentation describes `reqMktData()`, while the cancellation page documents `cancelMktData(tickerId)`. There is no end-marker callback analogous to `historicalDataEnd()`.

## Why threading appears now

Until this example, the course could simply do:

```python
app.connect(...)
app.run()
```

`app.run()` blocks while it processes incoming API messages. That was fine because each previous program ended from a callback.

For a long-lived subscription, we want the main thread to remain available so it can decide when to cancel the subscription or do other application work.

The example therefore starts the API processing loop on another thread:

```python
api_thread = Thread(target=app.run, name="ibkr-api")
api_thread.start()
```

The resulting structure is:

```text
Main thread
├── starts the API thread
├── waits while the subscription is active
├── cancelMktData(...)
├── disconnect()
└── joins the API thread

API thread
└── app.run()
    └── dispatches EWrapper callbacks

IBKR internal reader thread
└── receives socket messages
    └── places them on the Python API message queue
```

The distinction matters: the thread we create is the thread running `app.run()` and therefore dispatching callbacks. It is separate from the internal reader thread created by the Python API connection machinery.

## Waiting for connection readiness

Starting a background thread creates one new problem: the main thread must not assume that the connection is ready immediately.

The example uses a `threading.Event`:

```python
self.subscription_started = Event()
```

The subscription is started from the familiar readiness callback:

```python
def nextValidId(self, orderId: int) -> None:
    self.reqMktData(...)
    self.subscription_started.set()
```

and the main thread waits for that signal:

```python
app.subscription_started.wait(timeout=5)
```

This avoids relying on an arbitrary `sleep(1)` after `connect()`.

## Run the example

From the repository root:

```powershell
uv run python examples/03_market_data/streaming_market_data.py
```

During the ten-second subscription you should see price and size callbacks such as:

```text
PRICE  reqId=2  BID=...
SIZE   reqId=2  BID_SIZE=...
PRICE  reqId=2  ASK=...
SIZE   reqId=2  ASK_SIZE=...
```

The exact callbacks depend on the market state and your market-data permissions.

The next chapter explains the numeric tick types and their meanings. Market-data types and entitlement behavior are covered later in the market-data section.

## Official references

- [Requesting market data](https://www.interactivebrokers.com/docs/tws-api/doc/quick-start/requesting-market-data)
- [Cancel watchlist data](https://www.interactivebrokers.com/docs/tws-api/doc/market-data-live/top-of-book-l-1/cancel-watchlist-data)
- [TWS API architecture](https://www.interactivebrokers.com/docs/tws-api/doc/architecture/introduction)
