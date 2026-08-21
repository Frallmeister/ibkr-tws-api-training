# Modifying and cancelling orders

> **Status:** Planned

## Purpose
Explain how working orders are changed or cancelled and what callbacks confirm the resulting lifecycle.

## Intended coverage
- modifying with `placeOrder()` using the same order ID;
- cancellation requests;
- cancellation/status callbacks;
- race conditions with fills;
- why local intent and broker-confirmed state are different.

## Depends on
Order lifecycle.

## Leads into
More realistic order-management behavior and robustness.
