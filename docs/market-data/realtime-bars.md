# Real-time bars

`reqRealTimeBars()` provides a streaming sequence of completed **5-second bars**.

This makes it different from both market-data ticks and a finite historical-bar request:

```text
reqMktData()          -> individual fields update asynchronously
reqHistoricalData()   -> finite sequence of historical bars
reqRealTimeBars()     -> continuing sequence of 5-second bars
```

The runnable example is:

```text
examples/03_market_data/realtime_bars.py
```

It subscribes to NVDA real-time bars, prints several completed bars, cancels the subscription, and disconnects.

## The request

A basic stock request looks like this:

```python
self.reqRealTimeBars(
    reqId=REQUEST_ID,
    contract=create_stock_contract(),
    barSize=5,
    whatToShow="TRADES",
    useRTH=True,
    realTimeBarsOptions=[],
)
```

The important parameters are:

| Parameter | Meaning |
| --- | --- |
| `reqId` | Identifies this subscription in later callbacks |
| `contract` | Instrument whose bars should be streamed |
| `barSize` | Kept as `5`; this interface delivers 5-second bars |
| `whatToShow` | Selects the data source used to construct each bar |
| `useRTH` | If `True`, exclude data outside regular trading hours |
| `realTimeBarsOptions` | Reserved for special/internal options; use an empty list here |

IBKR's current [real-time-bar request reference](https://www.interactivebrokers.com/docs/tws-api/protobuf/real-time-bars-request) documents `barSize` as currently ignored. The interface nevertheless delivers fixed 5-second bars, so using `5` keeps the intent explicit and matches the established API usage.

## What comes back?

Each completed bar arrives through `EWrapper.realtimeBar()`:

```python
def realtimeBar(
    self,
    reqId,
    time,
    open_,
    high,
    low,
    close,
    volume,
    wap,
    count,
):
    ...
```

The callback contains the familiar OHLC fields together with additional values:

| Argument | Meaning |
| --- | --- |
| `reqId` | Which real-time-bar subscription produced the bar |
| `time` | Bar timestamp as Unix epoch seconds |
| `open_` | Opening value |
| `high` | Highest value |
| `low` | Lowest value |
| `close` | Closing value |
| `volume` | Traded volume when applicable |
| `wap` | Weighted average price |
| `count` | Number of trades represented by the bar |

IBKR's [real-time-bar callback reference](https://www.interactivebrokers.com/docs/tws-api/protobuf/real-time-bar-tick) is the authoritative field list.

For `whatToShow="TRADES"`, the callback therefore gives you a compact completed bar rather than forcing the application to assemble OHLC values from individual ticks.

## Fixed 5-second cadence

The defining property of `reqRealTimeBars()` is that the bars are **5 seconds long**.

Conceptually:

```text
09:30:00 ----- 09:30:05  -> realtimeBar(...)
09:30:05 ----- 09:30:10  -> realtimeBar(...)
09:30:10 ----- 09:30:15  -> realtimeBar(...)
...
```

This is not a general bar-size selector. You cannot ask this interface directly for a 1-minute or 5-minute bar by changing `barSize`.

If an application needs a larger interval, it can aggregate successive 5-second bars itself, or use another IBKR market-data interface where appropriate.

## Choosing `whatToShow`

`whatToShow` controls which underlying data is used to construct the bars.

For this stock example we use:

```python
whatToShow="TRADES"
```

That is the natural choice when you want bars based on executed trades.

Other values exist for other purposes. Rather than duplicating the complete reference here, use IBKR's documentation when choosing the [historical/real-time bar data source](https://www.interactivebrokers.com/docs/tws-api/doc/market-data-historical/historical-bars/receiving-historical-bars).

## `useRTH`

The `useRTH` flag controls whether data outside regular trading hours is included:

```python
useRTH=True
```

means the subscription should only include regular trading hours.

```python
useRTH=False
```

allows eligible data outside regular trading hours as well.

This parameter changes which observations can contribute to the bars; it does not change the 5-second cadence.

## Subscription lifecycle

Like `reqMktData()`, this is a long-lived subscription. There is no natural final bar that ends the request.

```text
reqRealTimeBars(3, ...)
        ↓
realtimeBar(3, ...)
realtimeBar(3, ...)
realtimeBar(3, ...)
...
        ↓
cancelRealTimeBars(3)
```

Cancel it explicitly with the same request ID:

```python
self.cancelRealTimeBars(REQUEST_ID)
```

This request-ID pattern should now be familiar:

```text
request ID -> identifies the subscription
callback   -> carries the same ID back
cancel     -> uses that ID to stop the subscription
```

## Real-time bars versus raw ticks

`reqMktData()` and `reqRealTimeBars()` are both streaming interfaces, but they provide different abstractions.

### `reqMktData()`

Produces field-level updates such as:

```text
BID
ASK
LAST
BID_SIZE
ASK_SIZE
...
```

Use it when the application needs current quote/trade fields or wants to react to updates at the tick-field level.

### `reqRealTimeBars()`

Produces already aggregated 5-second OHLC-style bars.

Use it when the application naturally works with short bars and does not need to reconstruct them from raw tick updates.

Neither interface is universally better; they expose different views of the market-data stream.

## Real-time bars versus historical bars

The callback payload looks similar to historical OHLC bars, but the lifecycle is different.

A normal `reqHistoricalData()` request is finite:

```text
historicalData(...)
historicalData(...)
...
historicalDataEnd(...)
```

A `reqRealTimeBars()` request continues until cancelled:

```text
realtimeBar(...)
realtimeBar(...)
...
```

There is also a third pattern worth knowing: `reqHistoricalData(..., keepUpToDate=True)` can continue updating historical-style bars through `historicalDataUpdate()`. IBKR describes that interface as a historical-data stream kept current with real-time updates. See [Receiving Historical Bars](https://www.interactivebrokers.com/docs/tws-api/doc/market-data-historical/historical-bars/receiving-historical-bars) for the authoritative behavior.

For this chapter, keep the distinction simple:

```text
reqHistoricalData()             -> historical bar workflow
reqRealTimeBars()               -> dedicated fixed 5-second stream
reqMktData()                    -> field/tick workflow
```

## Run the example

From the repository root:

```powershell
uv run python examples/03_market_data/realtime_bars.py
```

During the subscription you should see output shaped like:

```text
BAR reqId=3 time=... open=... high=... low=... close=... volume=... wap=... count=...
```

The exact values depend on the instrument, market state, trading session, and available market data.

The next chapter covers market-data types and permissions. That is where delayed versus live data and entitlement behavior belong.

## Official references

- [RealTimeBars request](https://www.interactivebrokers.com/docs/tws-api/protobuf/real-time-bars-request)
- [RealTimeBar callback fields](https://www.interactivebrokers.com/docs/tws-api/protobuf/real-time-bar-tick)
- [Receiving Historical Bars](https://www.interactivebrokers.com/docs/tws-api/doc/market-data-historical/historical-bars/receiving-historical-bars)
