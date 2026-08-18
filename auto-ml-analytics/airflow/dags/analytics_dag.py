from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
import yaml
import sys
sys.path.append('/opt/airflow/scripts')
from alerting import check_anomalies

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'analytics_dag',
    default_args=default_args,
    schedule_interval='0 6 * * *',
    catchup=False,
    max_active_runs=1,
    doc_md='''Ежедневный пайплайн аналитики: dbt run, тесты, ML предсказания, аномалии'''
) as dag:

    start = DummyOperator(task_id='start')

    # Загрузка данных (если нужно – можем пропустить, если уже есть)
    # generate_data = BashOperator(...)

    # Динамический запуск dbt моделей (из конфига)
    with open('/opt/airflow/config/dbt_vars.yml') as f:
        config = yaml.safe_load(f)
        models = config['models']

    previous_task = start
    for model in models:
        run_model = BashOperator(
            task_id=f'dbt_run_{model}',
            bash_command=f'cd /opt/airflow/dbt && dbt run --models {model} --profiles-dir .'
        )
        previous_task >> run_model
        previous_task = run_model

    # Запуск тестов dbt
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/dbt && dbt test --profiles-dir .'
    )

    # ML предсказания
    ml_predict = BashOperator(
        task_id='ml_predict_ltv',
        bash_command='python /opt/airflow/ml/predictions/predict_ltv.py'
    )

    # Аномали-детекшн
    anomaly_check = PythonOperator(
        task_id='anomaly_check',
        python_callable=check_anomalies
    )

    previous_task >> dbt_test >> ml_predict >> anomaly_check
