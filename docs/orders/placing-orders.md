# Placing a basic stock order

> **Status:** Planned

## Purpose
Show the smallest correct paper-trading order submission and trace the outbound command and inbound lifecycle callbacks.

## Intended coverage
- selecting a resolved stock contract;
- obtaining/using an order ID;
- `placeOrder()`;
- paper-trading safety;
- immediate callbacks and expected state transitions;
- avoiding strategy logic.

## Depends on
The `Order` object, contracts, and identifiers.

## Leads into
Order lifecycle, modification, cancellation, and executions.
