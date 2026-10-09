# ADR 001: reconciliation is an operational control

## Decision

Materialise daily source-to-warehouse reconciliation as a dbt model and expose its status to
operators.

## Context

A successful task does not prove that a complete dataset was loaded. Count and revenue
reconciliation makes loss or duplication visible independently of orchestration status.
