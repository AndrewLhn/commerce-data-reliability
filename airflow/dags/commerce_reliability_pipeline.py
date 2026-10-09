from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="commerce_reliability_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    max_active_runs=1,
    default_args={"owner": "data-engineering", "retries": 2, "retry_delay": timedelta(minutes=5)},
    tags=["commerce", "reliability", "dbt"],
) as dag:
    ingest_orders = BashOperator(
        task_id="ingest_synthetic_orders",
        bash_command="LOGICAL_DATE={{ ds }} python /opt/airflow/scripts/generate_synthetic_orders.py",
    )
    build_models = BashOperator(
        task_id="build_reliability_models",
        bash_command="cd /opt/airflow/dbt && dbt build --profiles-dir .",
    )
    ingest_orders >> build_models
