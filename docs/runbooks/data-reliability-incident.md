# Runbook: data reliability incident

1. Identify the failed date and rule in `mart_data_reliability_slo`.
2. Compare the raw order count with `ops.ingestion_runs` and the fact count.
3. Re-run the affected Airflow logical date after correcting configuration or source data.
4. Confirm reconciliation passes before resolving the incident.
