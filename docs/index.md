# IBKR TWS API Training

This site is a focused guide to the native Interactive Brokers TWS API in Python.

The objective is not to hide the API behind a production wrapper. The objective is to understand the machinery that a future trading application would rely on: the connection to TWS, the `EClient`/`EWrapper` split, asynchronous callbacks, request identifiers, contracts, market data, account state, orders, executions, and errors.

## Scope

The examples use U.S. stocks, primarily NASDAQ-listed equities. This keeps the material aligned with a realistic stock-trading use case while avoiding unrelated complexity from options, futures, forex, and multi-leg instruments.

The guide also avoids strategy development. A page may request NVDA historical bars or submit a paper-trading limit order, but it will not attempt to decide *when* NVDA should be bought.

## How to use this guide

The recommended workflow is:

1. read the conceptual explanation;
2. follow the request/callback flow;
3. inspect the runnable example;
4. run it against a TWS paper-trading session;
5. vary one thing at a time and observe the result;
6. use the linked IBKR documentation to inspect the full API contract.

The examples intentionally start small. Early examples keep `EClient` and `EWrapper` visible rather than introducing abstractions before there is a concrete problem for those abstractions to solve.

## Planned progression

### Fundamentals

- TWS, IB Gateway, and the Python process
- the message-oriented architecture
- `EClient` and `EWrapper`
- the network/event loop
- request IDs, order IDs, and client IDs
- common callback patterns
- the core IBKR object model

### Stock workflows

- defining and resolving stock contracts
- historical bars
- streaming market data
- accounts and positions
- order submission, modification, and cancellation
- executions and fills
- error handling and reconnect behavior

## Safety while learning

Use a paper-trading session for examples that can place or modify orders. Keep live trading disabled until you understand the request lifecycle, order identifiers, order-state callbacks, and failure modes well enough to reason about what the application will do when messages are delayed, duplicated, rejected, or interrupted.
