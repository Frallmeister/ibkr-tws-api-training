# Installation and environment setup

This repository uses `uv` to manage its Python environment, MkDocs, Ruff, and other normal Python dependencies. The native IBKR Python client is different: Interactive Brokers distributes it with the TWS API download.

## 1. Clone the repository

```powershell
git clone https://github.com/Frallmeister/ibkr-tws-api-training.git
cd ibkr-tws-api-training
```

## 2. Create the uv environment

Synchronize the locked project dependencies:

```powershell
uv sync --locked
```

This creates the repository-local virtual environment and installs the documentation and development tooling from `uv.lock`.

At this point the environment does **not** necessarily contain `ibapi`.

## 3. Install the official IBKR Python client

The supported TWS API Python source is included in the TWS API download. On a default Windows installation, the Python package source is commonly located under:

```text
C:\TWS API\source\pythonclient
```

Install that local package into this repository's uv environment:

```powershell
uv pip install "C:\TWS API\source\pythonclient"
```

If your TWS API is installed elsewhere, use the corresponding `pythonclient` path.

Verify the import:

```powershell
uv run python -c "import ibapi; print(ibapi.__file__)"
```

The printed path should resolve to the environment used by this repository.

## Why `ibapi` is not in `uv.lock`

`uv.lock` records dependencies that `uv` can resolve from the project's declared dependency sources. We deliberately do not declare the old `ibapi` package from PyPI as the training dependency because IBKR's supported distribution is the TWS API download.

That gives the environment this shape:

```text
uv-managed environment
├── MkDocs
├── Material for MkDocs
├── Ruff
└── ibapi  ← installed separately from IBKR's local pythonclient source
```

## Important: exact synchronization can remove `ibapi`

A normal `uv sync` performs an exact synchronization. Packages that are installed in the environment but are not declared by the project can be removed. Because the locally installed IBKR client is intentionally outside the lockfile, this matters here.

After installing `ibapi`, use either of these approaches:

### Preserve separately installed packages

```powershell
uv sync --locked --inexact
```

`--inexact` keeps packages that are not part of the locked project dependency set.

### Or reinstall `ibapi` after an exact sync

```powershell
uv sync --locked
uv pip install "C:\TWS API\source\pythonclient"
```

For day-to-day work you normally do not need to synchronize the environment before every command. Commands such as:

```powershell
uv run mkdocs serve
uv run ruff check .
uv run python examples/01_connection/current_time.py
```

run inside the existing project environment.

## If you already use the TWS API in another project

Keep that project independent. There is no requirement for every Python project on the machine to share one `ibapi` installation.

For this training repository, the cleanest arrangement is to install the official `pythonclient` into this repository's own `.venv`. That lets you experiment freely without changing the dependency environment of a future trading application.

## Python version

The repository currently supports Python 3.11 and newer at the project level. The actual interpreter used for an IBKR example must also be compatible with the particular TWS API Python client you downloaded.

The CI workflow uses Python 3.11 for deterministic documentation and lint checks. CI does not install `ibapi` because it does not execute examples that require a running TWS instance.
