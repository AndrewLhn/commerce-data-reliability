select distinct on (order_id)
  order_id, customer_id, order_date, amount, currency, ingested_at
from {{ ref('stg_orders') }}
order by order_id, ingested_at desc
