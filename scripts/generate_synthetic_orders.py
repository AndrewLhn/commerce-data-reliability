import os
import random
import uuid
from datetime import date

import psycopg2
from psycopg2.extras import execute_values

logical_date = os.environ.get("LOGICAL_DATE", date.today().isoformat())
random.seed(logical_date)
orders = [
    (str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{logical_date}-{index}")), f"customer-{index % 25:03d}", logical_date, round(random.uniform(15, 500), 2), "USD")
    for index in range(100)
]

connection = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "postgres"),
    dbname=os.environ["POSTGRES_DB"],
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
)
with connection, connection.cursor() as cursor:
    execute_values(
        cursor,
        "INSERT INTO raw.orders (order_id, customer_id, order_date, amount, currency) VALUES %s "
        "ON CONFLICT (order_id) DO NOTHING",
        orders,
    )
    cursor.execute(
        "INSERT INTO ops.ingestion_runs (logical_date, source_row_count, loaded_row_count, rejected_row_count, status, completed_at) VALUES (%s, %s, %s, 0, 'succeeded', now())",
        (logical_date, len(orders), len(orders)),
    )
