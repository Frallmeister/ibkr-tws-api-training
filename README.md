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

## Tooling

This repository uses [uv](https://docs.astral.sh/uv/) for environment and dependency management and [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.

Create/synchronize the environment from the repository root:

```powershell
uv sync
```

Run the documentation site locally:

```powershell
uv run mkdocs serve
```

Run the checks used for the Python examples:

```powershell
uv run ruff check .
uv run ruff format --check .
```

To apply Ruff formatting locally:

```powershell
uv run ruff format .
```

The project currently declares Python `>=3.11` rather than requiring Python 3.14 specifically. Newer Python versions can be used when the locally installed IBKR API is compatible with them.

> The Interactive Brokers TWS API package itself is installed separately using the official IBKR distribution. The examples assume that `ibapi` is importable in the uv-managed environment. We deliberately do not depend on the stale `ibapi` package published on PyPI.

## Documentation

The course is built with [MkDocs](https://www.mkdocs.org/) and Material for MkDocs.

After `uv sync`, start it with:

```powershell
uv run mkdocs serve
```

Then open the local address printed by MkDocs.

## Learning philosophy

Each topic is developed in this order:

1. establish the mental model;
2. identify the relevant IBKR objects;
3. trace the request and callback lifecycle;
4. inspect a minimal clean example;
5. run it against TWS paper trading;
6. consult the official IBKR documentation for the complete API contract.

The goal is to understand *why* the API is structured as it is, not merely to reproduce snippets that happen to work.
