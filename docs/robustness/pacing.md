# Pacing limits and request constraints

> **Status:** Planned

## Purpose
Explain that some TWS API requests are rate-limited or constrained by IBKR and that correct client code must respect those operational rules.

## Intended coverage
- pacing as a broker/API constraint rather than a Python performance problem;
- historical-data request limits;
- market-data subscription limits where relevant;
- interpreting pacing-related errors;
- avoiding retry loops that make a violation worse;
- consulting current IBKR limits because values can change.

## Depends on
Historical data, streaming data, and error handling.

## Leads into
Responsible long-running API usage.
