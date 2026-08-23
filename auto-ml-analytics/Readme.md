AutoML Analytics Platform

Overview
This repository delivers a production‑ready analytics platform for an e‑commerce business. It ingests raw transactional data, transforms it through 50+ complex SQL models (dbt), trains and serves ML models (LTV, churn, demand), and monitors everything with Prometheus/Grafana. All orchestration is handled by Apache Airflow, and the entire stack runs in Docker.

Architecture
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   Data Lake     │      │   PostgreSQL    │      │   Airflow       │
│  (Mock Data)    │ ───> │   (Warehouse)   │ ───> │   Orchestrator  │
└─────────────────┘      └─────────────────┘      └─────────────────┘
                                 │                          │
                                 ▼                          ▼
                         ┌─────────────────┐      ┌─────────────────┐
                         │   dbt Models    │      │   ML Training   │
                         │  (SQL Layers)   │      │  (sklearn)      │
                         └─────────────────┘      └─────────────────┘
                                 │                          │
                                 ▼                          ▼
                         ┌─────────────────┐      ┌─────────────────┐
                         │   Marts /       │      │   Predictions   │
                         │   ML Features   │      │   & Alerts      │
                         └─────────────────┘      └─────────────────┘
                                 │                          │
                                 └──────────┬───────────────┘
                                            ▼
                                     ┌─────────────────┐
                                     │   Grafana /     │
                                     │   Prometheus    │
                                     └─────────────────┘

Tech Stack 

Orchestration: Apache Airflow 2.7 (CeleryExecutor)

Data Warehouse: PostgreSQL 14

Transformations: dbt Core 1.5 (Postgres adapter)

Machine Learning: scikit‑learn, pandas, pickle

Monitoring: Prometheus + Grafana + Alertmanager

Containerisation: Docker & Docker Compose

Language: Python 3.10 + SQL (50+ dbt models)


Project Structure

├── dbt/                     # 50+ SQL models (staging, intermediate, marts, ml_features)
│   ├── models/
│   ├── macros/              # reusable window/cohort functions
│   ├── tests/               # generic & custom data quality tests
│   └── seeds/               # static reference data
├── ml/
│   ├── training/            # LTV, churn, demand model trainers
│   ├── predictions/         # daily inference scripts
│   ├── monitoring/          # performance metrics (MAE, RMSE)
│   └── artifacts/           # saved model pickles and metrics
├── scripts/
│   ├── generate_data.py     # creates millions of synthetic records
│   ├── alerting.py          # Telegram alerts for anomalies
│   └── init_db.sql
├── airflow/
│   ├── dags/
│   │   ├── analytics_dag.py         # dynamic DAG (generated from config)
│   │   └── ml_retraining_dag.py
│   └── plugins/
│       └── ml_operator.py   # custom Airflow operator for model training
├── config/
│   ├── dbt_vars.yml         # model list and parameters
│   └── ml_models.yaml       # target variables, feature sets
├── monitoring/              # Prometheus/Grafana/Alertmanager configs
└── reports/                 # auto‑generated daily HTML/PDF reports