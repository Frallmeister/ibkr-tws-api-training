# Historical bars example

This example requests one month of daily NVDA bars from TWS.

Runnable file:

```text
examples/03_market_data/historical_bars.py
```

Run it from the repository root with TWS connected to paper trading:

```powershell
uv run python examples/03_market_data/historical_bars.py
```

## Complete script

```python
from ibapi.client import EClient
from ibapi.common import BarData
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper

REQUEST_ID = 1


def create_stock_contract() -> Contract:
    """Create the stock contract used by the historical-data request."""
    contract = Contract()
    contract.symbol = "NVDA"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "NASDAQ"
    return contract


class HistoricalBarsApp(EWrapper, EClient):
    """Request one month of daily historical bars for NVDA."""

    def __init__(self) -> None:
        EClient.__init__(self, wrapper=self)

    def nextValidId(self, orderId: int) -> None:
        """Request historical bars once the API connection is ready."""
        print(f"Connected. Next valid order ID: {orderId}")

        self.reqHistoricalData(
            reqId=REQUEST_ID,
            contract=create_stock_contract(),
            endDateTime="",
            durationStr="1 M",
            barSizeSetting="1 day",
            whatToShow="TRADES",
            useRTH=1,
            formatDate=1,
            keepUpToDate=False,
            chartOptions=[],
        )

    def historicalData(self, reqId: int, bar: BarData) -> None:
        """Print one historical bar returned for the request."""
        print(
            f"{reqId}  {bar.date}  "
            f"O={bar.open} H={bar.high} L={bar.low} C={bar.close} V={bar.volume}"
        )

    def historicalDataEnd(self, reqId: int, start: str, end: str) -> None:
        """Disconnect once all bars for the request have arrived."""
        print(f"Historical request {reqId} complete: {start} -> {end}")
        self.disconnect()


def main() -> None:
    app = HistoricalBarsApp()
    app.connect(host="127.0.0.1", port=7497, clientId=1)
    app.run()


if __name__ == "__main__":
    main()
```

## What to observe

The request is finite:

```text
nextValidId(...)
    ↓
reqHistoricalData(1, ...)
    ↓
historicalData(1, bar)
historicalData(1, bar)
historicalData(1, bar)
    ...
    ↓
historicalDataEnd(1, ...)
    ↓
disconnect()
```

Each `historicalData()` callback contains one `BarData` object. The script prints its date, open, high, low, close, and volume.

The request uses:

```text
durationStr = "1 M"
barSizeSetting = "1 day"
whatToShow = "TRADES"
useRTH = 1
```

so the result is roughly one month of daily trade bars restricted to regular trading hours.

## Useful experiments

After the basic example works, change one request parameter at a time:

```python
durationStr = "2 W"
barSizeSetting = "1 hour"
whatToShow = "ADJUSTED_LAST"
useRTH = 0
```

Observe how the returned bars change while leaving the callback structure unchanged.

For the conceptual explanation of the request parameters and callbacks, see [Historical bars](../market-data/historical-bars.md).
