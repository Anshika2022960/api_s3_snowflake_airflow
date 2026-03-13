# Automated Data Pipeline: API → AWS S3 → Snowflake (Orchestrated with Airflow)

## Project Overview

This project demonstrates an end-to-end automated data pipeline that extracts data from an external API source, stores it in AWS S3, and loads it into Snowflake Data Warehouse using Snowpipe auto-ingestion. The entire workflow is orchestrated using Apache Airflow.

The goal of this project is to showcase how modern data engineering pipelines automate data ingestion, transformation, and loading for analytics and business intelligence.
The pipeline extracts user data from the following public API:https://api.freeapi.app/api/v1/public/randomusers?page=1&limit=500
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

   1. extracts user data from an API

   2. stores raw data in cloud storage

   3. loads data into Snowflake

   4. handles data quality issues

   5. prepares clean and usable data for analytics

## Tech Stack
- Python, Requests / Pandas, AWS S3, Snowflake, Snowpipe, Apache Airflow, SQL
## 🌐 API Used

This project uses the Random Users API: https://api.freeapi.app/api/v1/public/randomusers?page=1&limit=500
The API returns user-related data such as:
 - user ID
 - first name
 - last name
 - username
 - email
 - gender
 - date of birth
 - phone number
 - country
 - password

## End-to-End Workflow
## 1. Extract data from API

A Python script sends a request to the Random Users API and fetches up to 500 records.

Example:

import requests
url = "https://api.freeapi.app/api/v1/public/randomusers?page=1&limit=500"
response = requests.get(url)
data = response.json()

## 2. Save raw data

The extracted API response is saved as a raw file such as JSON or CSV.
Example output file: random_users_raw.csv

## 3. Upload raw data to AWS S3

The raw extracted file is uploaded into an AWS S3 bucket, which acts as the landing zone for the pipeline.

Example structure: s3://random-users-pipeline/raw/randomusers_api_data.csv

## 4. Snowpipe auto-ingestion

Snowpipe continuously monitors the S3 location and automatically loads the new file into Snowflake.

Flow: AWS S3 → Snowpipe → Snowflake Stage
## 5. Load data into staging table

The raw data is first loaded into a staging table in Snowflake.

This staging table is used to:

    - hold raw records

    - inspect data quality

    - perform cleaning before inserting into final tables

## 6. Clean the data

During implementation, the following issues were identified:

   Challenge 1: Null values in password

       Some records had null password values, which can create issues in downstream systems if password is expected to be populated.

   Challenge 2: Duplicate email addresses

      Some records contained duplicate email IDs, which can cause:

           1. duplicate customer profiles

           2. merge conflicts

           3. poor data quality in reporting systems

These issues were cleaned in the transformation step before loading into the final target table.

## Data Quality Challenges and Cleaning Approach
## 1. Handling null password values
  ## Problem

The password field had null values in some records.

  ## Why this is a problem

   - incomplete user records

   - bad data quality

   - issues in systems requiring mandatory fields

  ## Cleaning options

Depending on project requirement, null passwords can be handled by:

  1. Replacing null with a default placeholder

  2. Filtering out records with null password

  3. Marking them for review

## 2. Handling duplicate email addresses
 ## Problem

Some user records had duplicate email IDs.

 ## Why this is a problem

  1. Duplicate user entries

  2. Unreliable reporting

  3. Bad target table quality

  4. Issues in analytics or downstream applications

## ✅ Final Cleaning Logic

Before loading data into the target table, the following cleaning logic is applied:

  1.replace null password values using CASE WHEN expression

  2.remove duplicate emails using ROW_NUMBER()

  3.keep only valid, unique records

  4.merge cleaned data into the final target table

## 🔁 UPSERT into Target Table

After cleaning, the final data is merged into the target table.

## 📊 Real-World Learnings from This Project

This project helped demonstrate important data engineering concepts such as:

- Fuilding an API-based ingestion pipeline

- Storing raw data in cloud object storage

- Using Snowpipe for automated ingestion

- Designing staging and target layers

- Performing practical data cleaning

- Handling null and duplicate values

- preparing analytics-ready datasets

## 🚧 Challenges Faced
- Null password values

- Some records from the API contained missing password values, which required replacement using COALESCE() or filtering logic CASE WHEN.

- Duplicate emails

- Multiple records shared the same email ID, so deduplication logic had to be implemented using ROW_NUMBER().

- Data quality validation

- Raw API data cannot be directly trusted. Validation checks are necessary before loading into the final warehouse table.

## ✅ Outcome

- After implementing this pipeline:

- data was successfully extracted from the Random Users API

- raw records were stored in AWS S3

- Snowpipe ingested the files into Snowflake

- null password values were handled

- duplicate emails were removed

- clean user data was loaded into the final target table

## 📌 Key Features

- Automated API extraction

- Cloud storage using AWS S3

- Snowflake data warehousing

- Snowpipe auto-ingestion

- Airflow scheduling and orchestration

- Null handling for password field

- Deduplication based on email

- Final clean target table for analytics

## 🚀 Future Improvements

- Possible next enhancements:

- add data quality checks using Great Expectations

- use dbt for transformations

- add logging and monitoring in Airflow

- implement incremental load tracking

- create Power BI or Tableau dashboard on top of Snowflak
  
Automated ELT pipeline using Random Users API, AWS S3, Snowflake, Snowpipe, and Airflow with data cleaning for null passwords and duplicate emails.





