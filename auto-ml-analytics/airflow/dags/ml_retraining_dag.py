from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.append('/opt/airflow/ml/training')
from train_ltv import train_ltv

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'ml_retraining_dag',
    default_args=default_args,
    schedule_interval='0 4 * * 0',  # каждое воскресенье в 4 утра
    catchup=False,
    max_active_runs=1,
    doc_md='''Еженедельное переобучение ML моделей'''
) as dag:

    start = DummyOperator(task_id='start')

    # Сначала запускаем dbt модели для обновления признаков
    dbt_run_features = BashOperator(
        task_id='dbt_run_ml_features',
        bash_command='cd /opt/airflow/dbt && dbt run --models customer_ltv_features --profiles-dir .'
    )

    # Обучение модели LTV
    train_ltv_task = PythonOperator(
        task_id='train_ltv_model',
        python_callable=train_ltv
    )

    start >> dbt_run_features >> train_ltv_task
