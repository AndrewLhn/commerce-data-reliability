# Commerce Data Reliability

Local reference platform for monitoring the reliability of a daily e-commerce order pipeline.

~~~text
synthetic orders -> Airflow -> PostgreSQL raw -> dbt -> reconciliation and SLO marts -> Grafana
~~~

The platform records ingestion runs, compares source and warehouse totals, evaluates freshness and
data-quality rules, and stores failures as operational incidents.

## Core controls

- Idempotent daily synthetic-order loads.
- Run audit: received, loaded, rejected, and completion status.
- dbt models for orders, daily reconciliation, and reliability SLOs.
- Incident records for failed reconciliation or freshness checks.
- Versioned alert rules and dashboard queries.

## Local run

~~~bash
cp .env.example .env
docker compose up -d --build
~~~

Trigger `commerce_reliability_pipeline` in Airflow at http://localhost:8080.

## Models

| Model | Purpose |
| --- | --- |
| `stg_orders` | Typed raw orders |
| `fct_orders` | Current valid order facts |
| `mart_daily_reconciliation` | Source-to-warehouse volume and revenue comparison |
| `mart_data_reliability_slo` | Freshness, duplicate, and reconciliation status |

## Documentation

- [Architecture](docs/architecture.md)
- [SLO incident runbook](docs/runbooks/data-reliability-incident.md)
- [Reconciliation ADR](docs/adr/001-reconciliation-as-an-operational-control.md)
