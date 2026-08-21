# Request IDs, order IDs, and client IDs

> **Status:** Planned

## Purpose

Separate the identifier types that are often confused in TWS API examples and explain what each one correlates.

## Intended coverage

- `reqId` as request/response correlation;
- `orderId` as broker order identity within the API workflow;
- `clientId` as API-client identity for a TWS session;
- uniqueness expectations and ownership;
- `nextValidId()`;
- examples with concurrent requests;
- common identifier mistakes.

## Depends on

Callback patterns and connection lifecycle.

## Leads into

Contracts, market data, and orders.
