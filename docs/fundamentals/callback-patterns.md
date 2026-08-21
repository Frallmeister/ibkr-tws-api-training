# Requests, responses, subscriptions, and callback patterns

> **Status:** Planned

## Purpose

Turn the recurring interaction shapes of the TWS API into an explicit mental model.

## Intended coverage

- one request / one callback;
- one request / many callbacks / end marker;
- long-lived subscriptions;
- commands followed by lifecycle events;
- unsolicited events;
- when cancellation is required;
- sequence diagrams using the established compact Mermaid style.

## Depends on

Connection lifecycle and event loop.

## Leads into

Identifiers, historical data, streaming market data, orders, and executions.
