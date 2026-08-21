# Positions and portfolio state

> **Status:** Planned

## Purpose
Explain broker-reported holdings and how position callbacks differ from order and execution callbacks.

## Intended coverage
- `reqPositions()` and cancellation;
- `position()` and `positionEnd()`;
- contract information embedded in position callbacks;
- position quantity and average cost;
- multiple accounts where relevant;
- distinguishing current state from execution history.

## Depends on
Accounts, contracts, and callback patterns.

## Leads into
P&L and order/execution reconciliation.
