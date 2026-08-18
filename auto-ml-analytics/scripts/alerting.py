import os
import requests
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def send_telegram_alert(message):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if bot_token and chat_id:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": message})

def check_anomalies():
    engine = create_engine(os.getenv('DBT_DB_CONN'))
    # Проверяем выручку за последние 7 дней и сравниваем со средним за 30 дней
    df = pd.read_sql("""
        WITH daily_revenue AS (
            SELECT DATE(order_date) as day, SUM(total_price) as revenue
            FROM analytics.int_order_items_enriched
            GROUP BY day
        )
        SELECT 
            day,
            revenue,
            AVG(revenue) OVER (ORDER BY day ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS avg_30d,
            STDDEV(revenue) OVER (ORDER BY day ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS std_30d
        FROM daily_revenue
        ORDER BY day DESC
        LIMIT 7
    """, engine)
    
    for _, row in df.iterrows():
        if row['std_30d'] > 0 and abs(row['revenue'] - row['avg_30d']) > 3 * row['std_30d']:
            msg = f"⚠️ Anomaly: Revenue on {row['day']} = {row['revenue']} (avg 30d = {row['avg_30d']:.2f}, std = {row['std_30d']:.2f})"
            send_telegram_alert(msg)
            print(msg)
    print("✅ Anomaly check completed")
