# Using the official IBKR documentation

This guide is designed to **extend** the official Interactive Brokers material, not replace it.

Our job here is to make the TWS API easier to understand: build the mental model, explain why the API is structured the way it is, connect requests to callbacks, and provide small examples that are easy to reason about.

The official IBKR documentation remains the authoritative source for the exact API surface, supported parameters, object fields, error codes, version-dependent behavior, and changes over time.

A successful outcome of this course is therefore not only that you can write TWS API code. You should also become comfortable finding the corresponding information in IBKR's own resources.

## The resources to know

### TWS API documentation

Start with the current long-form TWS API documentation on IBKR Campus:

- [TWS API introduction](https://ibkrcampus.com/docs/tws-api/doc/introduction)

This documentation is best for understanding a **topic or workflow**: connectivity, contracts, market data, orders, and related behavior.

Use it when your question is something like:

> How does historical market data work?

or:

> What do I need to know before connecting an API client to TWS?

### TWS API reference

The TWS API reference is best when you already know the concept and need the exact shape of an API object or callback.

For example:

- [Contract class reference](https://ibkrcampus.com/docs/tws-api/ref/contract-class-reference/introduction)
- [ContractDetails class reference](https://ibkrcampus.com/docs/tws-api/ref/contract-details-class-reference)
- [Error codes](https://ibkrcampus.com/docs/tws-api/ref/error-codes)

Use the reference when your question is something like:

> What fields exist on `ContractDetails`?

or:

> What does error code 10090 mean?

A useful distinction is:

```text
Documentation → explain the concept and workflow
Reference     → look up the exact API contract
```

### IBKR API home

The [IBKR API home](https://ibkrcampus.com/campus/ibkr-api-page/ibkr-api-home/) is the broader entry point for Interactive Brokers' API ecosystem.

It links to the TWS API documentation, TWS API reference, changelog, training courses, and other IBKR APIs. It is useful when you need to re-orient yourself or find a resource whose exact location you do not remember.

### Python TWS API course

IBKR also publishes a [Python TWS API course](https://ibkrcampus.com/campus/traders-academy/api/).

It contains lessons on installation, API program structure, contracts, market data, orders, account data, scanners, and concurrency.

This course and the IBKR course serve different purposes. IBKR's material is valuable because it demonstrates the supported API directly. This guide spends more time explaining the architecture and relationships behind those examples so that the official material becomes easier to interpret.

### TWS API changelog

The API changes over time. When behavior, signatures, supported functionality, or documentation appear to disagree with an older example, consult the TWS API changelog from the [IBKR API home](https://ibkrcampus.com/campus/ibkr-api-page/ibkr-api-home/).

Do not assume that an old blog post, video, Stack Overflow answer, or legacy API page describes the current API exactly.

## A practical navigation workflow

Suppose you want to learn how contract discovery works.

A productive workflow is:

1. read our contracts chapter to understand what a `Contract` represents and why contract resolution exists;
2. open the relevant IBKR documentation to see the official workflow;
3. inspect the `Contract` and `ContractDetails` reference pages for their exact fields;
4. inspect the signatures for the relevant request and callbacks;
5. run our minimal example against paper TWS;
6. return to the reference whenever you need a field or parameter that our example does not use.

The same pattern applies throughout the guide:

```text
This guide
    ↓
understand the model
    ↓
IBKR documentation
    ↓
understand the official workflow
    ↓
IBKR reference
    ↓
look up exact methods, callbacks and fields
    ↓
run and modify the example
```

## Prefer current IBKR Campus material

You will still encounter the older `interactivebrokers.github.io/tws-api` documentation in search results and existing tutorials. Some of those pages remain useful, particularly for additional explanations and class-reference material, but IBKR marks that documentation as deprecated and directs users to IBKR Campus for current information.

In this guide, current IBKR Campus documentation is the default authority. If we link to a legacy page because it adds useful detail, we will identify it as such.

## How later chapters will use official references

Substantive chapters in this guide should end with a small **Official references** section containing the IBKR pages most relevant to that topic.

Those links are not optional footnotes. Following them is part of the learning process: over time you should need this guide less for lookup tasks because you know where IBKR documents the underlying API.
