# Automated Data Pipeline: API → AWS S3 → Snowflake (Orchestrated with Airflow)

## Project Overview

This project demonstrates an end-to-end automated data pipeline that extracts data from an external API source, stores it in AWS S3, and loads it into Snowflake Data Warehouse using Snowpipe auto-ingestion. The entire workflow is orchestrated using Apache Airflow.

The goal of this project is to showcase how modern data engineering pipelines automate data ingestion, transformation, and loading for analytics and business intelligence.
The pipeline extracts user data from the following public API:
https://api.freeapi.app/api/v1/public/randomusers?page=1&limit=500
The extracted data is stored in AWS S3, ingested into Snowflake using Snowpipe, and then cleaned and merged into the final target table.

This project also highlights practical data quality challenges faced during implementation, such as:

Null values in the password field

Duplicate email addresses

Cleaning and preparing data before final loading

It is a good example of a real-world ELT pipeline where raw data is first loaded and then cleaned inside the warehouse.




## Architecture Diagram
## Flow of the project

flowchart LR
    A[Random Users API] --> B[Python Extraction Script]
    B --> C[AWS S3 Bucket]
    C --> D[Snowpipe]
    D --> E[Snowflake Stage]
    E --> F[Staging Table]
    F --> G[Data Cleaning and Validation]
    G --> H[Target Table]

    I[Apache Airflow] --> B
    I --> C
    I --> D
    G --> B
    G --> C
## Project Objective

The main objective of this project is to build an automated data pipeline that:

extracts user data from an API

stores raw data in cloud storage

loads data into Snowflake

handles data quality issues

prepares clean and usable data for analytics

## Tech Stack
Tool / Technology	Purpose
Python	API extraction and preprocessing
Requests / Pandas	Fetch and process API data
AWS S3	Raw data storage
Snowflake	Data warehouse
Snowpipe	Auto-ingestion from S3
Apache Airflow	Workflow orchestration
SQL	Data cleaning, deduplication, and merge logic









