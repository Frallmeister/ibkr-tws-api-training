# IBKR TWS API Training

A focused learning resource for understanding the native Interactive Brokers TWS API in Python.

The repository is deliberately **not** a production trading framework. Its purpose is to make the API's architecture, object model, request/callback patterns, and stock-trading workflows understandable through clean documentation and small runnable examples.

It is designed to complement the official Interactive Brokers documentation. In addition to learning the API itself, the course aims to make the learner comfortable navigating IBKR Campus, using the TWS API reference, and consulting the official material directly for continued development.

## Scope

The material focuses on:

- the native `ibapi` Python package;
- TWS and IB Gateway as API hosts;
- U.S. equities, primarily NASDAQ-listed stocks;
- contracts and contract resolution;
- historical and streaming market data;
- accounts, positions, orders, executions, and errors;
- the asynchronous request/callback model;
- clean Python examples that keep the underlying API mechanics visible.

The material intentionally does **not** cover options, futures, forex, or strategy development.

## Getting started

The course is built with [MkDocs](https://www.mkdocs.org/) and Material for MkDocs. This repository uses [uv](https://docs.astral.sh/uv/) for environment and dependency management and [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.

The native Interactive Brokers Python client is supplied separately as part of the official TWS API distribution rather than as a supported PyPI dependency. The documentation explains how to install it into this repository's `uv` environment without hiding that distinction.

Start with the **Getting started** section in the documentation. It covers:

- installation and environment setup;
- TWS configuration for paper trading;
- running and checking the examples;
- how to use the official IBKR documentation and API reference alongside this course.

To serve the documentation after setting up the environment:

```powershell
uv run mkdocs serve
```

## Development checks

Run the same repository-level checks used by CI:

```powershell
uv run ruff check .
uv run ruff format --check .
uv run mkdocs build --strict
```

These checks do not execute TWS-connected examples. Running those examples requires the official `ibapi` installation and a running TWS paper-trading session.

## Learning philosophy

Each substantive topic is developed in this order:

1. establish the mental model;
2. identify the relevant IBKR objects;
3. trace the request and callback lifecycle;
4. inspect a minimal clean example;
5. run it against TWS paper trading;
6. consult the official IBKR documentation and reference for the complete API contract.

The goal is to understand *why* the API is structured as it is, not merely to reproduce snippets that happen to work. Over time, the learner should also become increasingly capable of using IBKR's own material directly for lookup and continued learning.
