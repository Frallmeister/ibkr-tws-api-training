# Getting started

This section prepares the local environment used by the examples in this guide.

The repository has two different dependency sources:

1. normal Python tooling such as MkDocs and Ruff, managed by `uv` from `pyproject.toml` and `uv.lock`;
2. the native IBKR Python client (`ibapi`), supplied by Interactive Brokers as part of the TWS API download rather than as a supported dependency from PyPI.

Keeping those two sources separate is intentional. The setup pages explain how to make them coexist without hiding where `ibapi` actually comes from.

## Recommended order

1. [Install the learning repository](installation.md).
2. [Configure TWS for API access](tws-configuration.md).
3. [Run and verify the local environment](running-examples.md).
4. Continue with the fundamentals chapters.

If you already have `ibapi` installed in another project, you do not need to change that project. The instructions here describe how to make the examples in **this repository** runnable in their own isolated `uv` environment.
