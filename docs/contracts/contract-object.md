# The `Contract` object

A stock symbol is not enough to describe a tradable instrument in the TWS API.

IBKR uses a `Contract` object to describe **what instrument an API operation refers to**.

For a U.S. stock, the familiar starting point is:

```python
from ibapi.contract import Contract

contract = Contract()
contract.symbol = "NVDA"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"
```

This object does not contain market data, an order, or a position. It is an instrument description that can be passed to API requests such as contract lookup, market-data requests, and orders.

## A `Contract` is a description

The important mental model is:

```text
Contract
   ↓
describes an instrument
   ↓
used by API operations that need to know
what should be looked up, priced, or traded
```

A `Contract` can be only partially specified or detailed enough to identify one specific instrument.

That distinction is fundamental to the TWS API.

## Core stock fields

For the stock workflows in this guide, the most important `Contract` fields are:

| Field | Meaning |
| --- | --- |
| `symbol` | The instrument symbol, for example `NVDA` |
| `secType` | Security type; `STK` means stock or ETF |
| `exchange` | The exchange or routing destination used by the API |
| `currency` | The contract currency, for example `USD` |
| `primaryExchange` | The instrument's primary listing exchange when needed for disambiguation |
| `conId` | IBKR's numeric contract identifier |

We will treat `primaryExchange` and `conId` separately later because they solve important identification and routing problems of their own.

For now, the key point is that IBKR identifies an instrument using **several properties**, not just its ticker symbol.

## Why the symbol alone is insufficient

Consider:

```python
contract = Contract()
contract.symbol = "ABC"
```

That tells IBKR very little.

The symbol does not state:

- whether the instrument is a stock;
- which currency is intended;
- which market or routing destination is relevant;
- whether another instrument shares the same or a similar symbol.

Adding fields narrows the description:

```python
contract.symbol = "NVDA"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"
```

Conceptually:

```text
symbol only
    ↓
broad description
    ↓
add security type
    ↓
add exchange/routing information
    ↓
add currency
    ↓
more specific contract description
```

The exact fields required depend on the API operation and whether the description is already unambiguous.

## Partial contracts are useful

A partially specified `Contract` is not necessarily wrong.

One important use is **contract resolution**. You can deliberately send a description to:

```python
self.reqContractDetails(reqId, contract)
```

and ask IBKR which contracts in its database match it.

The response then arrives through `ContractDetails` callbacks.

```mermaid
---
config:
  sequence:
    actorMargin: 24
    width: 100
    height: 36
    boxMargin: 4
    messageMargin: 22
    mirrorActors: false
    actorFontSize: 14px
    messageFontSize: 14px
    noteFontSize: 13px
---
sequenceDiagram
    participant App as Python application
    participant TWS

    App->>TWS: reqContractDetails(reqId, Contract)
    TWS-->>App: contractDetails(reqId, ContractDetails)
    TWS-->>App: contractDetailsEnd(reqId)
```

A broad description may match several contracts. A sufficiently specific description may match exactly one.

We will implement this lookup properly in the contract-resolution chapter.

## `Contract` versus `ContractDetails`

These two names are easy to confuse.

```text
Contract
= description of the instrument

ContractDetails
= IBKR metadata returned about a matched contract
```

A useful way to think about the flow is:

```text
your Contract description
        ↓
reqContractDetails(...)
        ↓
IBKR searches its contract database
        ↓
ContractDetails result
```

`ContractDetails` contains substantially more information than you normally provide when constructing a stock `Contract`, such as the resolved contract, valid exchanges, market rules, trading hours, and descriptive metadata.

That richer object belongs to the later resolution chapter.

## You normally construct the request object

Unlike many objects received through `EWrapper`, a `Contract` is commonly created by your own application:

```python
contract = Contract()
contract.symbol = "AAPL"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"
```

You then pass it into an `EClient` method.

So the direction is often:

```text
application
   ↓ creates
Contract
   ↓ passes to
EClient request or command
   ↓
TWS / IBKR
```

IBKR may later return `Contract` objects as part of other response objects as well, but the important starting case is that **your application describes the instrument it wants to operate on**.

## A `Contract` is not yet proof of identity

Creating this object:

```python
contract.symbol = "NVDA"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"
```

does not itself query IBKR or prove that the description resolves to the instrument you expect.

It is just a Python object until you pass it to an API operation.

That distinction matters:

```text
construct Contract
≠
resolve Contract against IBKR's database
```

The next chapters will make that process explicit.

## The mental model to keep

```text
Contract
├── identifies/describes what instrument you mean
├── is commonly constructed by your application
├── contains fields such as symbol, security type, exchange, and currency
├── may be partial or uniquely identifying
└── is passed into API operations that need an instrument
```

For this guide, the practical progression is:

```text
Contract object
      ↓
define a U.S. stock
      ↓
resolve it with reqContractDetails()
      ↓
understand SMART, primaryExchange, and conId
```

The next chapter turns this generic object into the standard contract definitions we will use for U.S. stocks throughout the rest of the course.

## Official references

- [Defining contracts in the TWS API](https://ibkrcampus.com/campus/trading-lessons/defining-contracts-in-the-tws-api/)
- [Contract details](https://www.interactivebrokers.com/docs/tws-api/doc/contracts-financial-instruments/contract-details/introduction)
- [TWS API Reference](https://www.interactivebrokers.com/docs/tws-api/ref/introduction)
