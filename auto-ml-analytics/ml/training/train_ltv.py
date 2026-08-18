import os
import pickle
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from datetime import datetime
import joblib

def train_ltv():
    engine = create_engine(os.getenv('DBT_DB_CONN'))
    df = pd.read_sql("""
        SELECT 
            customer_id,
            total_orders,
            avg_order_value,
            lifetime_value,
            recency_days,
            active_months
        FROM analytics.customer_ltv_features
        WHERE first_order_date < current_date - interval '90 days'
    """, engine)

    # Признаки и целевая переменная
    features = ['total_orders', 'avg_order_value', 'recency_days', 'active_months']
    X = df[features]
    y = df['lifetime_value']

    # Обучение модели
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Сохранение модели
    artifacts_path = os.getenv('ML_ARTIFACTS_PATH', '/opt/airflow/ml/artifacts')
    os.makedirs(artifacts_path, exist_ok=True)
    model_path = os.path.join(artifacts_path, 'ltv_model_rf.pkl')
    joblib.dump(model, model_path)

    # Метрики
    y_pred = model.predict(X)
    mae = mean_absolute_error(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    metrics = {
        'mae': mae,
        'rmse': rmse,
        'training_date': datetime.now().isoformat(),
        'n_samples': len(df)
    }
    metrics_path = os.path.join(artifacts_path, 'ltv_metrics.txt')
    with open(metrics_path, 'w') as f:
        for k, v in metrics.items():
            f.write(f"{k}: {v}\n")
    
    print(f"✅ LTV model trained, MAE: {mae:.2f}")
    return metrics
