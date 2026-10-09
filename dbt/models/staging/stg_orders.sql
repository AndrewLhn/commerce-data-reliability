select order_id, customer_id, order_date, amount, currency, ingested_at
from raw.orders
where amount >= 0
