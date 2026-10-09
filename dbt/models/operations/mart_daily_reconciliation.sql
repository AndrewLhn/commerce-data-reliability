with source_totals as (
  select logical_date, max(source_row_count) as source_row_count, max(loaded_row_count) as loaded_row_count
  from ops.ingestion_runs
  where status = 'succeeded'
  group by 1
),
warehouse_totals as (
  select order_date as logical_date, count(*) as warehouse_order_count, sum(amount) as warehouse_revenue
  from {{ ref('fct_orders') }}
  group by 1
)
select
  source_totals.logical_date,
  source_row_count,
  loaded_row_count,
  coalesce(warehouse_order_count, 0) as warehouse_order_count,
  source_row_count - coalesce(warehouse_order_count, 0) as order_count_difference,
  warehouse_revenue,
  case when source_row_count = coalesce(warehouse_order_count, 0) then 'passed' else 'failed' end as reconciliation_status
from source_totals
left join warehouse_totals using (logical_date)
