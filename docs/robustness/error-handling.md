# Error handling

> **Status:** Planned

## Purpose
Develop a disciplined approach to handling request errors, order rejections, warnings, and connection-level failures.

## Intended coverage
- categorizing messages from `error()`;
- request-scoped versus global failures;
- logging context such as request/order IDs;
- deciding when to retry, cancel, or stop;
- keeping examples understandable without swallowing errors.

## Depends on
Errors/messages and identifiers.

## Leads into
Reconnect behavior, pacing, and production-minded reasoning without building a production framework.
