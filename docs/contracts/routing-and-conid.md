# SMART routing, primary exchange, and `conId`

The fields `exchange`, `primaryExchange`, and `conId` all appear on a stock `Contract`, but they answer different questions.

For the U.S. stock workflows in this course:

```text
exchange
→ how the API operation should be routed

primaryExchange
→ where the stock is primarily listed

conId
→ IBKR's identifier for the specific contract
```

Keeping those three roles separate makes contract definitions much easier to reason about.

## Start from the contract-resolution example

The runnable example from the previous chapter already exposes all three concepts:

```powershell
uv run python examples/02_contracts/resolve_contract.py
```

It sends a stock description such as:

```python
contract.symbol = "NVDA"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"
```

and then prints fields from the resolved contract, including:

```text
exchange
primaryExchange
conId
validExchanges
```

This chapter explains what those returned values mean.

## `exchange = "SMART"` is a routing choice

For most U.S. stock examples in this repository, we use:

```python
contract.exchange = "SMART"
```

`SMART` refers to IBKR's SmartRouting framework. It tells IBKR that the operation should use smart routing rather than naming one specific execution venue directly.

It does **not** mean that the stock is listed on an exchange called SMART.

For example:

```python
contract.symbol = "AAPL"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"
contract.primaryExchange = "NASDAQ"
```

contains two different exchange-related ideas:

```text
SMART
→ routing

NASDAQ
→ primary listing exchange
```

There is no contradiction between them.

## `primaryExchange` helps identify the instrument

IBKR recommends including `primaryExchange` where possible because it can help distinguish contracts that would otherwise look ambiguous.

For example:

```python
contract.primaryExchange = "NASDAQ"
```

adds information about the identity of the stock. It does not tell IBKR to route the order only to NASDAQ.

That distinction is important:

```text
primaryExchange
≠
execution destination
```

The primary exchange is especially useful while you are still describing an instrument using human-readable fields such as:

```text
symbol
secType
currency
exchange
primaryExchange
```

A NASDAQ-listed stock and a NYSE-listed stock therefore use the same API structure:

```python
# NASDAQ-listed example
contract.symbol = "AAPL"
contract.primaryExchange = "NASDAQ"
```

```python
# NYSE-listed example
contract.symbol = "IBM"
contract.primaryExchange = "NYSE"
```

The listing venue changes; the contract model does not.

## `conId` identifies the resolved IBKR contract

After contract resolution, the returned `Contract` contains a numeric `conId`:

```python
resolved_contract = contractDetails.contract
print(resolved_contract.conId)
```

The `conId` is IBKR's contract identifier for that specific instrument.

This gives us two useful ways of referring to a stock.

A human-readable description:

```text
symbol = NVDA
secType = STK
exchange = SMART
currency = USD
primaryExchange = NASDAQ
```

or a resolved IBKR identity:

```text
conId = <resolved contract identifier>
exchange = SMART
```

IBKR's contract-management best-practices documentation recommends using the contract identifier together with the exchange once the instrument has been resolved.

Conceptually:

```text
human-readable description
        ↓
reqContractDetails(...)
        ↓
resolved Contract
        ↓
conId
        ↓
stable broker-side instrument identity
```

## Why `conId` is useful

A symbol is meaningful to a person, but it is not the strongest possible identity inside a broker API.

Consider what can vary around a symbol:

```text
security type
currency
listing venue
routing venue
instrument with a similar or reused symbol
```

A resolved `conId` removes much of that ambiguity because it refers directly to the contract in IBKR's database.

That is why the workflow in this course is:

```text
start with readable stock fields
        ↓
resolve the contract
        ↓
inspect conId and exchange metadata
        ↓
use the resolved identity confidently
```

## Defining a contract from a known `conId`

Once a `conId` is already known, a contract can be described much more directly.

For example:

```python
from ibapi.contract import Contract

contract = Contract()
contract.conId = resolved_con_id
contract.exchange = "SMART"
```

Here `resolved_con_id` would come from a prior contract-resolution result or another reliable IBKR contract source.

At that point you no longer need the symbol to establish which IBKR contract you mean.

The symbol can still be useful in your own application for readability, logging, or display, but it is no longer doing the core identification work.

## Do not invent a `conId`

A `conId` should come from IBKR.

Useful sources include:

```text
reqContractDetails(...)
IBKR contract search tools
other trusted IBKR contract metadata
```

Do not derive it from the symbol or maintain a guessed mapping.

The contract-resolution example gives us the native TWS API way to discover it:

```python
self.reqContractDetails(REQUEST_ID, contract)
```

followed by:

```python
contract = contractDetails.contract
print(contract.conId)
```

## `validExchanges` is related but different

The previous example also prints:

```python
contractDetails.validExchanges
```

This is metadata returned by IBKR describing exchange values that are valid for the resolved contract.

So these fields serve different purposes:

| Field | Role |
| --- | --- |
| `contract.exchange` | Routing/exchange value used for the contract operation |
| `contract.primaryExchange` | Primary listing exchange used as instrument-identification metadata |
| `contract.conId` | IBKR identifier for the resolved contract |
| `contractDetails.validExchanges` | Exchanges IBKR reports as valid for the contract |

We do not need to choose among individual execution venues yet. For the course examples, `SMART` remains the normal routing choice.

## A practical stock workflow

For a stock that your application knows only by symbol, the clean workflow is:

```text
1. Construct readable Contract

   symbol = NVDA
   secType = STK
   exchange = SMART
   currency = USD

2. Resolve with reqContractDetails()

3. Inspect returned Contract

   primaryExchange
   conId
   localSymbol
   tradingClass

4. Keep the resolved identity for later API operations
```

This separates two concerns:

```text
instrument discovery
→ which IBKR contract is this?

API operation
→ request data or submit an order for that contract
```

That separation becomes valuable in the next sections because market-data and order methods both accept `Contract` objects.

## The mental model to keep

```text
symbol
→ human-readable identifier

primaryExchange
→ helps disambiguate the listed instrument

conId
→ IBKR's contract identifier

SMART
→ routing choice for the API operation
```

Or, for a normal smart-routed U.S. stock:

```text
Instrument identity
├── conId
├── symbol
└── primaryExchange

Routing
└── exchange = SMART
```

The contracts section is now complete. The next section uses these resolved stock contracts to request market data.

## Official references

- [Defining contracts in the TWS API](https://www.interactivebrokers.com/campus/trading-lessons/defining-contracts-in-the-tws-api/)
- [Contract details](https://www.interactivebrokers.com/docs/tws-api/doc/contracts-financial-instruments/contract-details/introduction)
- [Contract management best practices](https://www.interactivebrokers.com/docs/general/contracts/contract-management/best-practices)
