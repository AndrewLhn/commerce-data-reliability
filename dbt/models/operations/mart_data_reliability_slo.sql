select
  logical_date,
  reconciliation_status,
  order_count_difference,
  warehouse_order_count,
  warehouse_revenue,
  case when reconciliation_status = 'passed' then 'passed' else 'failed' end as volume_slo_status,
  case when warehouse_revenue >= 0 then 'passed' else 'failed' end as revenue_slo_status
from {{ ref('mart_daily_reconciliation') }}
