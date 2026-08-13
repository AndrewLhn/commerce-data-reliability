-- Тест: LTV должен быть > 0
select customer_id
from {{ ref('customer_ltv_features') }}
where lifetime_value <= 0
