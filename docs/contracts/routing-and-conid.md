# SMART routing, primary exchange, and `conId`

A U.S. stock can be listed on one exchange but traded on many different venues.

For example, a NASDAQ-listed stock does not have to execute on NASDAQ. Its shares may also be available on other exchanges, electronic venues, or dark pools.

That is the problem SMART solves.

## What SMART actually does

When you use:

```python
contract.exchange = "SMART"
```

you are telling IBKR not to restrict the order to one specific execution venue.

Instead, IBKR's SmartRouting system evaluates competing venues and decides where to send the order. According to IBKR, the router continuously searches for available prices across exchanges and dark pools and can dynamically reroute all or part of an order as market conditions change.

Its routing decision can consider more than the displayed price, including transaction costs, exchange fees or rebates, available liquidity, and opportunities for price improvement.

Conceptually:

```text
Your order
   |
   v
IBKR SmartRouting
   |
   +--> venue A
   +--> venue B
   +--> venue C
   +--> dark pool
```

IBKR may choose one venue or route different portions of the order to different venues.

This is why `SMART` is not the name of an exchange. It means:

> Let IBKR choose the execution venue instead of directing the order to one venue yourself.

For the stock examples in this course, SMART will normally be the routing choice.

## Then what is `primaryExchange`?

`primaryExchange` answers a different question:

> Where is this stock primarily listed?

For example:

```python
contract.symbol = "NVDA"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"
contract.primaryExchange = "NASDAQ"
```

means:

```text
Instrument:       NVDA stock, primarily listed on NASDAQ
Order routing:    let IBKR SmartRoute it
```

NASDAQ helps identify the instrument. It does **not** force the order to execute on NASDAQ.

That is the key distinction:

```text
primaryExchange = identity
exchange         = routing
```

`primaryExchange` is especially useful when a symbol alone is ambiguous.

## `conId`: IBKR's own instrument identifier

The previous chapter resolved a human-readable contract with:

```python
self.reqContractDetails(REQUEST_ID, contract)
```

and IBKR returned a `Contract` containing a numeric `conId`.

A `conId` is IBKR's identifier for that specific contract.

So there are two different ways to identify the same stock.

Human-readable description:

```text
symbol = NVDA
secType = STK
currency = USD
primaryExchange = NASDAQ
```

IBKR-resolved identity:

```text
conId = <IBKR contract identifier>
```

The first form is convenient when humans construct or inspect a contract. The second is useful once IBKR has already resolved exactly which instrument you mean.

## Why `conId` is useful

A ticker is not a permanent broker-side identity.

Symbols can be ambiguous, reused, or require additional fields such as security type, currency, and listing exchange to identify the intended instrument.

`conId` points directly to the contract in IBKR's contract database.

After resolving a contract, you can therefore build a more direct contract such as:

```python
from ibapi.contract import Contract

contract = Contract()
contract.conId = resolved_con_id
contract.exchange = "SMART"
```

IBKR's contract-management guidance recommends using the resolved contract identifier together with the exchange.

Notice that these two fields still solve different problems:

```text
conId = which instrument?
SMART = how should an order be routed?
```

## See all three concepts in the existing example

Run:

```powershell
uv run python examples/02_contracts/resolve_contract.py
```

The example prints fields including:

```text
conId
exchange
primaryExchange
validExchanges
```

For a typical result, interpret them like this:

| Field | Meaning |
| --- | --- |
| `conId` | IBKR's identifier for the resolved instrument |
| `primaryExchange` | Primary listing exchange of the stock |
| `exchange` | Exchange/routing value on the returned contract |
| `validExchanges` | Venues IBKR reports as valid for that contract |

`validExchanges` is useful metadata, but we do not need to choose among those venues ourselves when using SMART routing.

## The model to keep

For the stock workflows in this course:

```text
Which instrument?
    conId
    symbol
    primaryExchange

How should the order reach the market?
    exchange = "SMART"
```

Or in one sentence:

> `primaryExchange` helps identify the listed stock, `conId` is IBKR's resolved identifier for it, and SMART lets IBKR choose where the order should actually execute.

The contracts section is now complete. The next section uses these contracts to request market data.

## Official references

- [Contract details](https://www.interactivebrokers.com/docs/tws-api/doc/contracts-financial-instruments/contract-details/introduction)
- [Contract management best practices](https://www.interactivebrokers.com/docs/general/contracts/contract-management/best-practices)
