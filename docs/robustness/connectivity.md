# Connectivity events and reconnect behavior

> **Status:** Planned

## Purpose
Explain how an API application observes connection loss, restoration, and TWS/IBKR connectivity events.

## Intended coverage
- socket disconnect versus farm/connectivity status messages;
- relevant error/status callbacks;
- what state may need to be re-requested after reconnect;
- avoiding assumptions that one successful `connect()` guarantees a permanent session;
- paper-trading experiments that do not place orders.

## Depends on
Connection lifecycle and errors/messages.

## Leads into
Robust long-running API processes.
