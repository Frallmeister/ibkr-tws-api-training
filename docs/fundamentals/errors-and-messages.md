# Errors, warnings, and informational messages

> **Status:** Planned

## Purpose

Explain the `error()` callback as a general API message channel rather than assuming every invocation is a fatal error.

## Intended coverage

- error callback signatures;
- request-specific versus connection-level messages;
- informational status messages and warnings;
- reading error codes and official documentation;
- deciding what should terminate an example;
- avoiding brittle code that treats every message identically.

## Depends on

Connection lifecycle and callback patterns.

## Leads into

Robustness, market-data permissions, and order rejection handling.
