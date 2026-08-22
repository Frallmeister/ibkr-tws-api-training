# Defining U.S. stock contracts

For the stock workflows in this guide, most `Contract` objects will start from the same four fields:

```python
from ibapi.contract import Contract

contract = Contract()
contract.symbol = "NVDA"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"
```

This is the standard shape we will reuse for U.S. equities throughout the course.

## The four core fields

```text
symbol   = which ticker
secType  = what kind of instrument
exchange = where/how IBKR should route the operation
currency = which currency
```

For a typical U.S. stock:

```python
contract.symbol = "AAPL"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"
```

IBKR's own contract lesson describes these four values as the basis of a normal contract definition.

## `secType = "STK"`

IBKR uses short security-type codes rather than Python subclasses such as `StockContract`.

For stocks and ETFs, the relevant value is:

```python
contract.secType = "STK"
```

So both an individual stock and an exchange-traded fund are represented with `STK` at this level.

The rest of this repository stays focused on this security type.

## `currency = "USD"`

For the U.S. equities used in this guide:

```python
contract.currency = "USD"
```

Currency is part of the contract description. It should not be inferred merely from the ticker symbol.

Conceptually:

```text
NVDA
+ STK
+ USD
```

is more specific than simply:

```text
NVDA
```

## `exchange = "SMART"`

For most examples we will use:

```python
contract.exchange = "SMART"
```

`SMART` means that the API operation uses IBKR's SmartRouting framework rather than naming one specific execution venue directly.

That is different from saying that the stock is **listed on an exchange called SMART**.

For example, an AAPL contract may be defined as:

```python
contract.symbol = "AAPL"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"
```

while AAPL's primary listing exchange is NASDAQ.

So keep these two ideas separate:

```text
exchange = "SMART"
→ routing destination used by the API

primaryExchange = "NASDAQ"
→ primary listing exchange of the instrument
```

We will study that distinction in more detail later.

## Adding `primaryExchange`

IBKR recommends including `primaryExchange` where possible because it can help distinguish otherwise ambiguous contracts.

For a NASDAQ-listed stock:

```python
contract = Contract()
contract.symbol = "AAPL"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"
contract.primaryExchange = "NASDAQ"
```

For a NYSE-listed stock, the same structure might instead use:

```python
contract = Contract()
contract.symbol = "IBM"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"
contract.primaryExchange = "NYSE"
```

The architecture is identical. NASDAQ is simply the primary exchange for many of the examples in this course; it is not a requirement of the TWS API.

## Why keep both `exchange` and `primaryExchange`?

They answer different questions.

```text
exchange
→ how/where the API operation is routed

primaryExchange
→ where the instrument is primarily listed
```

That is why a normal smart-routed U.S. stock contract can contain both:

```python
contract.exchange = "SMART"
contract.primaryExchange = "NASDAQ"
```

There is no contradiction between those fields.

## A reusable contract shape

For the NASDAQ-focused examples in this repository, you will repeatedly see objects shaped like this:

```python
contract = Contract()
contract.symbol = "MSFT"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"
contract.primaryExchange = "NASDAQ"
```

Changing the symbol gives another NASDAQ-listed stock:

```python
contract.symbol = "AMD"
```

The surrounding contract structure remains the same.

At this stage, it is better to keep this construction explicit rather than hide it behind a helper function. Seeing the individual fields makes later contract-resolution results easier to understand.

## Do not guess `primaryExchange`

`primaryExchange` is useful precisely because it contributes to instrument identity. It should therefore come from reliable instrument information rather than from an assumption based on the ticker.

If you are unsure, contract resolution is the appropriate next step:

```text
partial Contract
      ↓
reqContractDetails(...)
      ↓
resolved ContractDetails
      ↓
inspect returned Contract
```

That workflow is the subject of the next chapter.

## The mental model to keep

For a normal U.S. equity in this guide:

```text
Contract
├── symbol = "NVDA"
├── secType = "STK"
├── exchange = "SMART"
├── currency = "USD"
└── primaryExchange = "NASDAQ"   when known/useful
```

The important distinctions are:

- `STK` identifies the security type;
- `USD` is part of the contract description;
- `SMART` is a routing choice, not the stock's listing exchange;
- `primaryExchange` helps identify the actual listed instrument;
- NASDAQ is common in this course, but the same structure applies to NYSE-listed U.S. stocks.

The next chapter will turn this static contract definition into an actual API interaction by resolving a stock through `reqContractDetails()` and inspecting what IBKR returns.

## Official references

- [Defining contracts in the TWS API](https://www.interactivebrokers.com/campus/trading-lessons/defining-contracts-in-the-tws-api/)
- [How to define contracts using the Python TWS API](https://www.interactivebrokers.com/campus/ibkr-quant-news/how-to-define-contracts-using-the-python-tws-api/)
- [Contract details](https://www.interactivebrokers.com/docs/tws-api/doc/contracts-financial-instruments/contract-details/introduction)
