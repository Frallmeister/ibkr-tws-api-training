# Connection lifecycle and event loop

> **Status:** Planned

## Purpose

Explain what happens from `connect()` through the API handshake, message processing, callback dispatch, and disconnect.

## Intended coverage

- connection handshake and readiness;
- the role and blocking behavior of `run()`;
- message reading/decoding at the right conceptual depth;
- which thread executes callbacks;
- `nextValidId()` as a readiness signal;
- orderly disconnect behavior.

## Depends on

TWS API architecture; `EClient` and `EWrapper`.

## Leads into

Callback patterns, identifiers, streaming data, and reconnect behavior.
