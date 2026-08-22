# Running the examples

The examples are intentionally small standalone scripts. Run them from the repository root so commands and relative paths are consistent with the documentation.

## Verify the tooling

```powershell
uv run ruff check .
uv run ruff format --check .
uv run mkdocs build --strict
```

These checks do not require TWS or `ibapi` unless a future check explicitly imports an IBKR example.

## Verify `ibapi`

Before running an API example:

```powershell
uv run python -c "import ibapi; print(ibapi.__file__)"
```

If this fails, return to [Installation and environment setup](installation.md).

## Run an example

Current runnable examples include:

```powershell
uv run python examples/01_connection/current_time.py
uv run python examples/02_contracts/resolve_contract.py
```

Start TWS and log in to paper trading before running examples that connect to the API.

## Serve the documentation locally

```powershell
uv run mkdocs serve
```

MkDocs prints the local address for the development site. The server automatically rebuilds the documentation when Markdown files change.

## A useful experimentation pattern

The guide is tutorial-oriented rather than exercise-driven. After a documented example works, change one variable at a time and observe the result. Examples include changing a request ID, a contract field, a bar size, or a connection setting.

Keep experiments local unless they improve the canonical teaching example. The committed examples should remain small and focused on the API concept being taught.
