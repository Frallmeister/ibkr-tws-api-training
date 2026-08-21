# Partial fills

> **Status:** Planned

## Purpose
Explain how one order can be filled by multiple executions over time and how that affects order state.

## Intended coverage
- cumulative filled versus remaining quantity;
- multiple execution callbacks for one order;
- average fill price;
- interaction between `orderStatus()` and `execDetails()`;
- why applications should not assume one order equals one fill.

## Depends on
Executions and order lifecycle.

## Leads into
Commission information and robust order-state reasoning.
