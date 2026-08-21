# Contract resolution and `ContractDetails`

> **Status:** Planned

## Purpose
Explain how `reqContractDetails()` turns a partially specified stock contract into broker-resolved instrument information.

## Intended coverage
- request/callback/end-marker sequence;
- `ContractDetails` versus `Contract`;
- handling zero, one, or multiple matches;
- inspecting resolved identifiers and exchange information;
- using resolution as a learning tool rather than hiding it behind helpers.

## Depends on
U.S. stock contracts and callback patterns.

## Leads into
SMART routing, `conId`, historical data, and order submission.
