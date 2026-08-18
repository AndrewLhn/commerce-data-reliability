import os
import pandas as pd
import joblib
from sqlalchemy import create_engine

def predict_ltv():
    engine = create_engine(os.getenv('DBT_DB_CONN'))
    artifacts_path = os.getenv('ML_ARTIFACTS_PATH', '/opt/airflow/ml/artifacts')
    model_path = os.path.join(artifacts_path, 'ltv_model_rf.pkl')
    model = joblib.load(model_path)

    # Получаем клиентов, у которых нет LTV (или он NULL)
    df_new = pd.read_sql("""
        SELECT 
            customer_id,
            total_orders,
            avg_order_value,
            recency_days,
            active_months
        FROM analytics.customer_ltv_features
        WHERE lifetime_value IS NULL
    """, engine)

    if len(df_new) == 0:
        print("No new customers to predict")
        return

    features = ['total_orders', 'avg_order_value', 'recency_days', 'active_months']
    predictions = model.predict(df_new[features])
    df_new['predicted_ltv'] = predictions

    # Сохраняем во временную таблицу и обновляем основную
    df_new.to_sql('temp_ltv_pred', engine, if_exists='replace', index=False)
    with engine.begin() as conn:
        conn.execute("""
            UPDATE analytics.customer_ltv_features AS target
            SET lifetime_value = temp.predicted_ltv
            FROM temp_ltv_pred AS temp
            WHERE target.customer_id = temp.customer_id
        """)
    
    print(f"✅ LTV predictions saved for {len(df_new)} customers")
