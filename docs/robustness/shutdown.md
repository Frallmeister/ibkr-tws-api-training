# Clean shutdown and subscription cancellation

> **Status:** Planned

## Purpose
Explain how examples and longer-running scripts should stop without leaving the lifecycle implicit.

## Intended coverage
- cancelling streaming subscriptions;
- disconnect order;
- allowing callbacks to finish where appropriate;
- behavior of `run()` after disconnect;
- separating clean shutdown from reconnect logic.

## Depends on
Connection lifecycle and subscription patterns.

## Leads into
A complete end-to-end understanding of API process lifecycle.
