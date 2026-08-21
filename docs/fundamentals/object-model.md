# Core IBKR object model

> **Status:** Planned

## Purpose

Introduce the recurring Python objects that represent broker-domain concepts before they appear across many workflows.

## Intended coverage

- `Contract` and `ContractDetails`;
- `Order` and `OrderState`;
- `Execution` and commission data;
- bar and tick data objects;
- objects constructed by the application versus objects returned by IBKR;
- how identifiers connect objects and callbacks.

## Depends on

EClient/EWrapper and callback patterns.

## Leads into

Contracts, market data, accounts, orders, and executions.
