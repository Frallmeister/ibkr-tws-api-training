# Using the official IBKR documentation

This guide is designed to **extend** the official Interactive Brokers material, not replace it.

Our goal is to make the TWS API easier to understand: establish the mental model, explain how requests and callbacks fit together, and provide small examples that are easy to reason about. IBKR's own documentation remains the authoritative source for the exact API surface.

By the end of the course, you should be comfortable moving from a concept explained here to the corresponding IBKR documentation and reference pages on your own.

## The resources to know

### TWS API documentation

Use the [TWS API documentation](https://www.interactivebrokers.com/docs/tws-api/doc/introduction) when you want to understand how a feature or workflow behaves.

Typical questions are:

> How does historical market data work?

> What happens when an API client connects to TWS?

### TWS API reference

Use the [TWS API reference](https://www.interactivebrokers.com/docs/tws-api/ref/introduction) when you already understand the concept and need exact class, field, method, or callback information.

For example:

- [Contract class reference](https://www.interactivebrokers.com/docs/tws-api/ref/contract-class-reference/introduction)
- [ContractDetails class reference](https://www.interactivebrokers.com/docs/tws-api/ref/contract-details-class-reference)
- [Error codes](https://www.interactivebrokers.com/docs/tws-api/ref/error-codes)

A useful distinction is:

```text
Documentation -> understand behavior and workflow
Reference     -> look up the exact API contract
```

### IBKR API home and Python course

The [IBKR API home](https://ibkrcampus.com/campus/ibkr-api-page/ibkr-api-home/) is a useful entry point for the broader API material, including documentation, reference pages, changelogs, and training resources.

IBKR also publishes a [Python TWS API course](https://ibkrcampus.com/campus/traders-academy/api/) with lessons covering the main API workflows.

## How to use these resources with this guide

Suppose you are learning contract discovery:

1. read our chapter to understand what a `Contract` represents and why contract resolution exists;
2. use the IBKR documentation for the official workflow;
3. use the API reference when you need exact `Contract` or `ContractDetails` fields;
4. run and modify the example against paper TWS.

That pattern applies throughout the course. Substantive chapters should therefore end with a short **Official references** section containing the most relevant IBKR pages.
