# Architecture

The pipeline ingests a deterministic daily order set into PostgreSQL and records each load in
`ops.ingestion_runs`. dbt builds typed facts, reconciles source counts with warehouse counts,
and materialises SLO status for operational use.

A mismatch is a data incident, not a silent dashboard discrepancy. The local reference stack is
deliberately small: Airflow orchestrates, PostgreSQL stores data and audit records, and dbt
expresses transformation and reliability controls.
