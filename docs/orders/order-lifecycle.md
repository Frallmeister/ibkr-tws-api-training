# `openOrder` and `orderStatus`

> **Status:** Planned

## Purpose
Explain that submitting an order begins a lifecycle rather than returning a final result.

## Intended coverage
- `openOrder()`;
- `orderStatus()`;
- `OrderState`;
- repeated and out-of-order status observations where relevant;
- distinguishing submitted, working, filled, cancelled, and rejected states;
- compact Mermaid sequence diagrams for lifecycle flows.

## Depends on
Placing a basic stock order and callback patterns.

## Leads into
Modification, cancellation, and executions.
