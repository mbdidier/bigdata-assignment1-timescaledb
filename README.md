# Assignment 1 – TimescaleDB Performance Analysis

This repository contains all materials for **Assignment 1** of the **Big Data Analytics** course.

## 📌 Project Overview
The project evaluates the performance of **TimescaleDB** for time-series energy data, focusing on:
- Chunking strategies (3-hour, 1-day, 1-week)
- Compression impact on storage and query performance
- Continuous aggregates for analytical workloads
- Visualization using Grafana

## 🏗️ Architecture
- Python publisher/subscriber for data ingestion
- EMQX as MQTT broker
- TimescaleDB (PostgreSQL) for storage
- Grafana for visualization
- Docker for deployment

## 📂 Repository Structure
- `src/` – Python scripts (publisher, subscriber)
- `sql/` – SQL scripts (schema, hypertables, compression, CAGGs)
- `docker/` – Docker Compose configuration
- `report/` – LaTeX source and final PDF report
- `screenshots/` – Evidence screenshots (Grafana, compression, query timing)

## ▶️ How to Run
1. Start services:
   ```bash
   docker compose up -d
