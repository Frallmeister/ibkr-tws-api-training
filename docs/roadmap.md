# Course roadmap

This page defines the intended progression of the guide. It is both a learner-facing map and a guardrail for future development.

The course stays focused on the **native IBKR TWS API in Python for U.S. stocks**, primarily NASDAQ-listed equities. It teaches API concepts and workflows, not trading-strategy design.

## Status legend

- **Available** — substantive material exists and is ready to study.
- **Planned** — the page exists to record scope and sequencing, but the chapter has not been written yet.

## 1. Getting started

**Status: Available**

Establish the local environment and TWS prerequisites before introducing more API concepts.

- Installation and environment setup
- TWS API configuration
- Running the examples

## 2. Fundamentals

Build the mental model that makes the rest of the API predictable.

- **Available:** TWS API architecture
- **Available:** `EClient` and `EWrapper`
- **Planned:** Connection lifecycle and event loop
- **Planned:** Requests, responses, subscriptions, and callback patterns
- **Planned:** Request IDs, order IDs, and client IDs
- **Planned:** Core IBKR object model
- **Planned:** Errors, warnings, and informational messages

## 3. Contracts and stock identification

Understand how IBKR represents a tradable U.S. equity before requesting data or placing orders.

- **Planned:** The `Contract` object
- **Planned:** Defining U.S. stock contracts
- **Planned:** Contract resolution and `ContractDetails`
- **Planned:** SMART routing, primary exchange, and `conId`

## 4. Market data

Learn the main historical and streaming data interfaces used for stocks.

- **Planned:** Historical bars
- **Planned:** Streaming market data
- **Planned:** Tick types and attributes
- **Planned:** Real-time bars
- **Planned:** Market-data types and permissions

## 5. Accounts and positions

Inspect broker/account state independently of strategy logic.

- **Planned:** Accounts and account values
- **Planned:** Positions and portfolio state
- **Planned:** P&L subscriptions

## 6. Orders

Learn the stock-order lifecycle in paper trading.

- **Planned:** The `Order` object
- **Planned:** Placing a basic stock order
- **Planned:** `openOrder` and `orderStatus`
- **Planned:** Modifying and cancelling orders
- **Planned:** Market, limit, stop, and stop-limit orders
- **Planned:** Attached and bracket orders
- **Planned:** Time in force and outside-RTH behavior

## 7. Executions and fills

Distinguish submitted orders from actual executions.

- **Planned:** Executions and `execDetails`
- **Planned:** Partial fills
- **Planned:** Commission information

## 8. Robustness and operating constraints

Study behavior that matters when scripts run for longer than a toy example.

- **Planned:** Connectivity events and reconnect behavior
- **Planned:** Error handling
- **Planned:** Pacing limits and request constraints
- **Planned:** Clean shutdown and subscription cancellation

## 9. Reference

Cross-cutting material intended to support the rest of the guide.

- **Planned:** Terminology and definitions
- **Planned:** Callback-pattern reference
- **Planned:** Official IBKR documentation map

## Development rule

A planned page should not be expanded merely because an API feature is interesting. New material should follow this roadmap unless there is a clear pedagogical reason to change the sequence. If the roadmap changes, update this page first so the intended structure remains explicit.
