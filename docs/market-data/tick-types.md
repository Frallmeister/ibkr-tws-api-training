# Tick types and attributes

A `reqMktData()` subscription does not return one quote object. Instead, IBKR sends separate callback events for the fields that change.

The `tickType` argument tells you what each callback value means.

## Tick type identifiers

Consider the two callbacks already used in the streaming example:

```python
from decimal import Decimal

from ibapi.common import TickAttrib
from ibapi.ticktype import TickTypeEnum


def tickPrice(
    self,
    reqId: int,
    tickType: int,
    price: float,
    attrib: TickAttrib,
) -> None:
    print(reqId, TickTypeEnum.toStr(tickType), price)


def tickSize(self, reqId: int, tickType: int, size: Decimal) -> None:
    print(reqId, TickTypeEnum.toStr(tickType), size)
```

Here the callback arguments answer different questions:

| Argument | Meaning |
| --- | --- |
| `reqId` | Which market-data subscription produced the update? |
| `tickType` | Which market-data field is being updated? |
| `price` or `size` | What is the new value? |
| `attrib` | What additional properties apply to this price tick? |

IBKR represents tick types with integer identifiers. For example:

| Tick type | ID | Callback |
| --- | ---: | --- |
| `BID_SIZE` | 0 | `tickSize()` |
| `BID` | 1 | `tickPrice()` |
| `ASK` | 2 | `tickPrice()` |
| `ASK_SIZE` | 3 | `tickSize()` |
| `LAST` | 4 | `tickPrice()` |
| `LAST_SIZE` | 5 | `tickSize()` |
| `HIGH` | 6 | `tickPrice()` |
| `LOW` | 7 | `tickPrice()` |
| `VOLUME` | 8 | `tickSize()` |
| `CLOSE` | 9 | `tickPrice()` |
| `OPEN` | 14 | `tickPrice()` |

The complete list is much larger. The important pattern is that the numeric identifier is part of the protocol, while your application normally wants a meaningful name.

## Use `TickTypeEnum` instead of magic numbers

You could write:

```python
if tickType == 1:
    print("Bid", price)
```

but this hides the meaning of `1`.

The Python API exposes `TickTypeEnum`, so code can instead use named constants:

```python
if tickType == TickTypeEnum.BID:
    print("Bid", price)
```

and convert arbitrary identifiers to readable names:

```python
tick_name = TickTypeEnum.toStr(tickType)
```

This is why the streaming example can print output such as:

```text
PRICE  reqId=2  BID=...
SIZE   reqId=2  BID_SIZE=...
PRICE  reqId=2  ASK=...
SIZE   reqId=2  ASK_SIZE=...
```

## Price ticks and size ticks are separate events

A bid quote is not delivered as one `(price, size)` object.

Instead, IBKR can send separate events:

```text
tickPrice(reqId=2, tickType=BID, ...)
tickSize(reqId=2, tickType=BID_SIZE, ...)
```

The same applies to ask and last-trade data.

This matters when building application state later. A callback tells you that one field changed; it does not necessarily provide a complete synchronized quote snapshot.

A simple application might therefore maintain state such as:

```python
quote = {
    "bid": None,
    "bid_size": None,
    "ask": None,
    "ask_size": None,
    "last": None,
}
```

and update only the field represented by each incoming `tickType`.

That state-building pattern is introduced later. For now, focus on interpreting the callback correctly.

## Standard fields versus generic ticks

In the streaming example we use:

```python
genericTickList=""
```

That requests the standard market-data fields that IBKR normally returns for the contract.

IBKR also supports additional fields through the `genericTickList` argument. Those fields are requested using separate numeric identifiers supplied as a comma-separated string.

For example:

```python
genericTickList="232"
```

requests an additional generic tick defined by IBKR.

Do not confuse these two uses of numeric identifiers:

- `genericTickList` controls some additional data requested from IBKR;
- the `tickType` callback argument identifies the field that IBKR is delivering back to you.

For normal bid, ask, last, size, high, low, volume, close, and open fields, the empty generic tick list is sufficient.

## What is `TickAttrib`?

`tickPrice()` contains one argument that `tickSize()` does not:

```python
attrib: TickAttrib
```

`TickAttrib` is metadata describing properties of that price tick. It does not replace `tickType` and it is not another market-data value.

For `reqMktData()` price callbacks, the relevant attributes include:

| Attribute | Meaning |
| --- | --- |
| `canAutoExecute` | Whether the quote is available for automatic execution |
| `pastLimit` | Whether the price is outside certain daily price boundaries described by IBKR |
| `preOpen` | Whether a bid/ask quote is from a pre-open state |

You can inspect them directly:

```python
def tickPrice(self, reqId, tickType, price, attrib):
    print(
        TickTypeEnum.toStr(tickType),
        price,
        attrib.canAutoExecute,
        attrib.pastLimit,
        attrib.preOpen,
    )
```

For an ordinary first market-data consumer, the price itself and the tick type are usually the primary pieces of information. The attributes become useful when the application needs to reason more carefully about the status or provenance of a quote.

## Reading a callback from left to right

Suppose the API invokes:

```text
tickPrice(2, 1, 181.42, attrib)
```

You can interpret it systematically:

1. `reqId=2` — this belongs to subscription 2;
2. `tickType=1` — `TickTypeEnum.BID`, so this is a bid-price update;
3. `price=181.42` — the new bid price is 181.42;
4. `attrib` — additional metadata qualifies that price tick.

Likewise:

```text
tickSize(2, 3, 400)
```

means:

1. subscription 2;
2. tick type 3 = `ASK_SIZE`;
3. the ask-size field has been updated to the supplied size value.

This is the central mental model for `reqMktData()` callbacks:

```text
request ID  -> which subscription?
tick type   -> which field?
value       -> what changed?
attributes  -> what qualifies the value?
```

## What to observe in the existing example

Run:

```powershell
uv run python examples/03_market_data/streaming_market_data.py
```

and compare the output with `TickTypeEnum` and IBKR's available-tick-types table.

You should notice that:

- several different tick types can belong to the same `reqId`;
- price-related fields arrive through `tickPrice()`;
- size-related fields arrive through `tickSize()`;
- not every possible field is guaranteed to appear during every run;
- `TickTypeEnum.toStr()` makes the raw identifiers much easier to interpret.

The exact fields and update timing depend on the instrument, market state, and available market data.

## Official references

- [Available tick types](https://www.interactivebrokers.com/docs/tws-api/doc/market-data-live/available-tick-types/introduction)
- [Requesting market data](https://www.interactivebrokers.com/docs/tws-api/doc/quick-start/requesting-market-data)
