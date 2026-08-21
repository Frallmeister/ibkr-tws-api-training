# Streaming market data

> **Status:** Planned

## Purpose
Explain long-lived market-data subscriptions and how tick callbacks differ from finite historical requests.

## Intended coverage
- `reqMktData()` and cancellation;
- `tickPrice()`, `tickSize()`, and related callbacks;
- subscription lifecycle;
- request ID correlation;
- bid, ask, last, and volume concepts;
- why a subscription has no single return value.

## Depends on
Historical bars, callback patterns, and identifiers.

## Leads into
Tick types, real-time bars, and permissions.
