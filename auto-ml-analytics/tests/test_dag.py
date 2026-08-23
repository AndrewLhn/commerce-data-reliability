from airflow.models import DagBag
import pytest

def test_dag_loaded():
    dag_bag = DagBag()
    assert dag_bag.dags["analytics_dag"] is not None
    assert len(dag_bag.import_errors) == 0

def test_ml_retraining_dag_loaded():
    dag_bag = DagBag()
    assert dag_bag.dags["ml_retraining_dag"] is not None
    assert len(dag_bag.import_errors) == 0

def test_analytics_dag_structure():
    dag = DagBag().dags["analytics_dag"]
    tasks = dag.task_dict
    assert "start" in tasks
    assert any("dbt_run" in t for t in tasks)
    assert "dbt_test" in tasks
    assert "ml_predict_ltv" in tasks
    assert "anomaly_check" in tasks
