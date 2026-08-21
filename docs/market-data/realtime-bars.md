# Real-time bars

> **Status:** Planned

## Purpose
Explain IBKR's real-time bar subscription separately from raw market-data ticks and historical bars.

## Intended coverage
- `reqRealTimeBars()`;
- fixed bar interval semantics;
- callback lifecycle and cancellation;
- relationship to historical bars and tick streams;
- when the interface is useful for stock applications.

## Depends on
Streaming market data and historical bars.

## Leads into
Choosing appropriate market-data interfaces.
