# First connection: request the server time

The first runnable example should prove the architecture with as little unrelated API surface as possible.

We therefore request the current IBKR server time. This gives us:

- a real connection to TWS;
- an outbound `EClient` request;
- an inbound `EWrapper` callback;
- the API processing loop;
- a clean termination point;
- no contracts, market-data permissions, or orders yet.

The runnable file is:

```text
examples/01_connection/current_time.py
```

## Before running the example

Complete the [installation and environment](../getting-started/installation.md) and [TWS configuration](../getting-started/tws-configuration.md) steps first.

This example uses:

```python
host = "127.0.0.1"
port = 7497
clientId = 1
```

These are connection settings, not API constants. The configured values in your TWS session are authoritative.

## The complete example

```python
from datetime import datetime

from ibapi.client import EClient
from ibapi.wrapper import EWrapper


class CurrentTimeApp(EWrapper, EClient):
    """Minimal TWS API application that requests the IBKR server time."""

    def __init__(self) -> None:
        EClient.__init__(self, wrapper=self)

    def nextValidId(self, orderId: int) -> None:
        """Called when the API connection is ready for requests."""
        print(f"Connected. Next valid order ID: {orderId}")
        self.reqCurrentTime()

    def currentTime(self, time: int) -> None:
        """Handle the server-time response and end the example."""
        server_time = datetime.fromtimestamp(time).astimezone()
        print(f"IBKR server time: {server_time.isoformat()}")
        self.disconnect()


def main() -> None:
    app = CurrentTimeApp()
    app.connect(host="127.0.0.1", port=7497, clientId=1)
    app.run()


if __name__ == "__main__":
    main()
```

## Trace the lifecycle

### 1. Construct the application

```python
app = CurrentTimeApp()
```

The object combines the outbound `EClient` interface with the inbound `EWrapper` callbacks.

Inside `__init__`:

```python
EClient.__init__(self, wrapper=self)
```

initializes the client side and tells it to dispatch wrapper callbacks to this same object.

### 2. Open the socket connection

```python
app.connect(host="127.0.0.1", port=7497, clientId=1)
```

This initiates the API connection to the local TWS process.

The `clientId` identifies this API client within the TWS session. We will study client IDs separately because they become important when several programs connect to the same TWS instance and when dealing with orders.

### 3. Start processing API messages

```python
app.run()
```

This is a crucial line.

The TWS API is event-driven. Opening the connection is not enough; the application also needs to process incoming network messages so they can be decoded and dispatched to `EWrapper` callbacks.

For this first example we let `run()` occupy the main thread. That is the simplest possible arrangement and makes the lifecycle easy to see. Later we will examine the event loop and threading in more detail.

### 4. Wait for connection readiness

Eventually the API invokes:

```python
def nextValidId(self, orderId: int) -> None:
```

Despite its name, `nextValidId()` is useful for more than learning an order ID. It is also an important connection-lifecycle callback: receiving it tells us that the connection handshake has progressed far enough for the application to start issuing API requests.

For that reason this example does **not** do this:

```python
app.connect(...)
app.reqCurrentTime()
app.run()
```

Instead the request is made from the readiness callback:

```python
def nextValidId(self, orderId: int) -> None:
    self.reqCurrentTime()
```

That makes the ordering explicit.

### 5. Send the request

This line is an `EClient` operation:

```python
self.reqCurrentTime()
```

Conceptually:

```mermaid
flowchart LR
    App["CurrentTimeApp"] -->|"EClient.reqCurrentTime()"| TWS["TWS"]
```

There is no useful return value containing the time.

### 6. Receive the response

After TWS responds and the API decodes the message, it invokes:

```python
def currentTime(self, time: int) -> None:
```

Conceptually:

```mermaid
flowchart LR
    TWS["TWS"] -->|"Current-time message"| Decoder["Message decoder"]
    Decoder --> Wrapper["EWrapper.currentTime(...)"]
    Wrapper --> App["CurrentTimeApp.currentTime(...)"]
```

Our override converts the Unix timestamp to a timezone-aware local `datetime` and prints it.

### 7. Disconnect

The example has achieved its purpose after one response, so the callback calls:

```python
self.disconnect()
```

Once the connection is closed, `run()` can finish and the process exits normally.

This is different from a streaming-market-data application, where the event loop may remain active for the entire trading session.

## Run it

From the repository root:

```powershell
uv run python examples/01_connection/current_time.py
```

A successful run can look like this:

```text
Connected. Next valid order ID: 1
ERROR -1 ... 2104 Market data farm connection is OK:usfarm
ERROR -1 ... 2106 HMDS data farm connection is OK:euhmds
IBKR server time: 2026-08-22T01:50:02+02:00
```

The exact order ID, timestamp, farm names, and number of status messages will differ.

### Why do successful runs print `ERROR`?

IBKR sends warnings, status notifications, and genuine errors through the same error-message mechanism. Codes `2104` and `2106` are normal connection-status notifications: they report that market-data and historical-data farms are connected.

The `-1` indicates that the message is not associated with one specific API request.

This also shows an important property of the API: messages from different parts of the TWS session can arrive between a request and its response. In the run above, connection-status messages arrive after `nextValidId()` and before `currentTime()`.

We leave those messages visible in this first example rather than filtering them out. Error handling and message classification are covered later in the guide.

## Things to inspect yourself

While TWS is running, change one thing at a time and observe the behavior:

- use the wrong port;
- temporarily disable API socket clients in TWS;
- change `clientId`;
- add a print before and after `app.run()`;
- remove `disconnect()` and observe that the program keeps processing messages.

The goal is not to create a better application yet. It is to develop an accurate intuition for the connection and callback lifecycle.

## What we deliberately did not introduce

This first example contains no:

- background thread;
- queue;
- `asyncio`;
- custom broker abstraction;
- request manager;
- contract object;
- market-data subscription;
- order placement.

Those concepts will be introduced only when they solve a concrete problem that we have already observed in the native API.
