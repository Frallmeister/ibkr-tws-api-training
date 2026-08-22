# Contract resolution example

This example resolves a partial NVDA stock description against IBKR's contract database.

Runnable file:

```text
examples/02_contracts/resolve_contract.py
```

Run it from the repository root with TWS connected to paper trading:

```powershell
uv run python examples/02_contracts/resolve_contract.py
```

## Complete script

```python
from ibapi.client import EClient
from ibapi.contract import Contract, ContractDetails
from ibapi.wrapper import EWrapper

REQUEST_ID = 1


def create_stock_contract() -> Contract:
    """Create the stock description that will be resolved by IBKR."""
    contract = Contract()
    contract.symbol = "NVDA"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    return contract


class ContractResolutionApp(EWrapper, EClient):
    """Resolve a stock description and print the matching IBKR contracts."""

    def __init__(self) -> None:
        EClient.__init__(self, wrapper=self)
        self.match_count = 0

    def nextValidId(self, orderId: int) -> None:
        """Request contract details once the API connection is ready."""
        print(f"Connected. Next valid order ID: {orderId}")
        self.reqContractDetails(REQUEST_ID, create_stock_contract())

    def contractDetails(self, reqId: int, contractDetails: ContractDetails) -> None:
        """Print one contract that matched the request."""
        self.match_count += 1
        contract = contractDetails.contract

        print(f"\nMatch {self.match_count} for request {reqId}")
        print(f"  symbol: {contract.symbol}")
        print(f"  conId: {contract.conId}")
        print(f"  secType: {contract.secType}")
        print(f"  exchange: {contract.exchange}")
        print(f"  primaryExchange: {contract.primaryExchange}")
        print(f"  currency: {contract.currency}")
        print(f"  localSymbol: {contract.localSymbol}")
        print(f"  tradingClass: {contract.tradingClass}")
        print(f"  longName: {contractDetails.longName}")
        print(f"  validExchanges: {contractDetails.validExchanges}")

    def contractDetailsEnd(self, reqId: int) -> None:
        """End the example after all matches for the request have arrived."""
        print(f"\nRequest {reqId} complete. Matches: {self.match_count}")
        self.disconnect()


def main() -> None:
    app = ContractResolutionApp()
    app.connect(host="127.0.0.1", port=7497, clientId=1)
    app.run()


if __name__ == "__main__":
    main()
```

## What to observe

The important sequence is:

```text
nextValidId(...)
    ↓
reqContractDetails(1, contract)
    ↓
contractDetails(1, ...)
    ↓
contractDetailsEnd(1)
    ↓
disconnect()
```

`contractDetails()` may be called more than once because the request can match multiple contracts. `contractDetailsEnd()` tells the application that IBKR has finished returning matches for request `1`.

The returned object also shows the difference between the description you sent and the richer contract information IBKR resolved, including fields such as `conId`, `primaryExchange`, `localSymbol`, and `tradingClass`.

## Useful experiments

Change one field at a time and run the script again. For example:

```python
contract.symbol = "AAPL"
```

or deliberately make the description less specific and observe whether the number of matches changes.

For the conceptual explanation behind this API flow, see [Contract resolution and `ContractDetails`](../contracts/contract-resolution.md).
