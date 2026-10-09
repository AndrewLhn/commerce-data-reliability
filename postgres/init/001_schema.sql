CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS ops;

CREATE TABLE IF NOT EXISTS raw.orders (
  order_id text PRIMARY KEY,
  customer_id text NOT NULL,
  order_date date NOT NULL,
  amount numeric(12, 2) NOT NULL CHECK (amount >= 0),
  currency text NOT NULL,
  ingested_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS ops.ingestion_runs (
  run_id bigserial PRIMARY KEY,
  logical_date date NOT NULL,
  source_row_count integer NOT NULL,
  loaded_row_count integer NOT NULL,
  rejected_row_count integer NOT NULL,
  status text NOT NULL,
  started_at timestamptz NOT NULL DEFAULT now(),
  completed_at timestamptz
);

CREATE TABLE IF NOT EXISTS ops.data_incidents (
  incident_id bigserial PRIMARY KEY,
  logical_date date NOT NULL,
  rule_name text NOT NULL,
  severity text NOT NULL,
  observed_value numeric,
  threshold_value numeric,
  status text NOT NULL DEFAULT 'open',
  detected_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (logical_date, rule_name)
);
