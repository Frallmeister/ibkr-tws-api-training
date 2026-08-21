# IBKR TWS API Training

A focused learning resource for understanding the native Interactive Brokers TWS API in Python.

The repository is deliberately **not** a production trading framework. Its purpose is to make the API's architecture, object model, request/callback patterns, and stock-trading workflows understandable through clean documentation and small runnable examples.

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

This repository uses [uv](https://docs.astral.sh/uv/) for its normal Python dependencies and environment management. The official IBKR Python client is installed separately from the TWS API download.

Start with the **Getting started** section in the MkDocs site for the complete setup, including the important interaction between `uv sync` and the separately installed `ibapi` package.

Create the locked project environment:

```powershell
uv sync --locked
```

Run the documentation site locally:

```powershell
uv run mkdocs serve
```

## Tooling

Run the local quality checks with:

```powershell
uv run ruff check .
uv run ruff format --check .
uv run mkdocs build --strict
```

To apply Ruff formatting locally:

```powershell
uv run ruff format .
```

The project currently declares Python `>=3.11`. Newer Python versions can be used when the locally installed IBKR API is compatible with them.

> The Interactive Brokers TWS API package itself is installed separately using the official IBKR distribution. We deliberately do not depend on the stale `ibapi` package published on PyPI.

## Course roadmap

The documentation contains an explicit roadmap covering:

1. getting started;
2. fundamentals;
3. contracts and stock identification;
4. market data;
5. accounts and positions;
6. orders;
7. executions and fills;
8. robustness;
9. reference material.

Planned pages are included in the navigation with notes describing their intended purpose, coverage, dependencies, and place in the learning sequence. They are deliberately marked as planned until substantive material is written.

## Learning philosophy

Each topic is developed in this order:

1. establish the mental model;
2. identify the relevant IBKR objects;
3. trace the request and callback lifecycle;
4. inspect a minimal clean example;
5. run it against TWS paper trading;
6. consult the official IBKR documentation for the complete API contract.

The goal is to understand *why* the API is structured as it is, not merely to reproduce snippets that happen to work.
