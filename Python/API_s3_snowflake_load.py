from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import pandas as pd
import boto3
import io
import snowflake.connector



# ========== Configuration ==========
url = "https://api.freeapi.app/api/v1/public/randomusers?page=1&limit=500"
bucket_name = "monalisa-123"
s3_file_name = "data/randomusers_api_data.csv "

#============= AWS credentials==========
aws_access_key = "xxxxxxxxxxxx"
aws_secret_access_key = "xxxxxxxxxxxxxxxxxxxx"
region_name = "ap-south-1"

# ===============STEP 1:Fetch API and save CSV==========================

def fetch_and_save_api_data_csv():

     response = requests.get(url)
     json_data = response.json()
     user_records = json_data["data"]["data"]

# Step 2: Normalize JSON to pandas DataFrame
     df = pd.json_normalize(user_records)
     print(" Proper DataFrame (Rows and Columns):")

# count number of columns and their name in api data
     column_count = len(df.columns)
     column_names = df.columns.tolist()

     print(column_count, column_names)

     csv_buffer = io.StringIO()
     df.to_csv(csv_buffer, index=False)

#===================STEP 2: UPLOAD TO S3===============================
def upload_to_s3():


  s3 = boto3.client(
     "s3",
      aws_access_key_id = aws_access_key,
      aws_secret_access_key = aws_secret_access_key,
      region_name = region_name
      )
# Upload file
  
  csv_buffer = io.StringIO()
  s3.put_object(Bucket=bucket_name, Key = s3_file_name, Body= csv_buffer.getvalue())

 
# print(df)
# print(f"CSV file saved locally as: {csv_buffer}")
print(f"csv_buffer.getvalue() uploaded successfully to s3:{bucket_name}")
#print(f" CSV File uploaded successfully to s3:{bucket_name}") 

 #========== STEP 3: Truncate and Load in Snowflake ==========
def s3_snowflake_truncate_and_load():

    conn = snowflake.connector.connect(
    user='MONALISADEV03',
    password='xxxxxxxxxx',
    account='CTXDFLT-BM46128', 
    warehouse='COMPUTE_WH',
    database='ETL_Project',
    schema="RAW",
    role="ACCOUNTADMIN"

    )
    cur = conn.cursor()
    # 1) Load csv files from stage into RAW table (VARIANT)
    cur.execute("TRUNCATE TABLE ETL_PROJECT.RAW.stage_target;")
    cur.execute("""
    COPY INTO ETL_PROJECT.RAW.stage_target
    FROM @ETL_PROJECT.RAW.my_stage
    FILE_FORMAT = (FORMAT_NAME = ETL_PROJECT.RAW.MY_CSV_FORMAT)
    ON_ERROR = 'CONTINUE';
    """)

     # Merge data from RAW table to  Final target table
    cur.execute("""
            MERGE INTO ETL_Project.ANALYTICS.final_target AS T
            USING ETL_Project.RAW.stage_target AS S
            ON T.LOGIN_UUID = S.LOGIN_UUID
            WHEN MATCHED THEN UPDATE SET
                T.GENDER = S.GENDER,
                T.EMAIL = S.EMAIL,
                T.PHONE = S.PHONE,
                T.CELL = S.CELL,
                T.ID = S.ID,
                T.NAT = S.NAT,
                T.NAME_TITLE = S.NAME_TITLE,
                T.NAME_FIRST = S.NAME_FIRST,
                T.NAME_LAST = S.NAME_LAST,
                T.LOCATION_STREET_NUMBER = S.LOCATION_STREET_NUMBER,
                T.LOCATION_STREET_NAME = S.LOCATION_STREET_NAME,
                T.LOCATION_CITY = S.LOCATION_CITY,
                T.LOCATION_STATE = S.LOCATION_STATE,
                T.LOCATION_COUNTRY = S.LOCATION_COUNTRY,
                T.LOCATION_POSTCODE = S.LOCATION_POSTCODE,
                T.LOCATION_COORDINATES_LATITUDE = S.LOCATION_COORDINATES_LATITUDE,
                T.LOCATION_COORDINATES_LONGITUDE = S.LOCATION_COORDINATES_LONGITUDE,
                T.LOCATION_TIMEZONE_OFFSET = S.LOCATION_TIMEZONE_OFFSET,
                T.LOCATION_TIMEZONE_DESCRIPTION = S.LOCATION_TIMEZONE_DESCRIPTION,
                T.LOGIN_USERNAME = S.LOGIN_USERNAME,
                T.LOGIN_PASSWORD = S.LOGIN_PASSWORD,
                T.LOGIN_SALT = S.LOGIN_SALT,
                T.LOGIN_MD5 = S.LOGIN_MD5,
                T.LOGIN_SHA1 = S.LOGIN_SHA1,
                T.LOGIN_SHA256 = S.LOGIN_SHA256,
                T.DOB_DATE = S.DOB_DATE,
                T.DOB_AGE = S.DOB_AGE,
                T.REGISTERED_DATE = S.REGISTERED_DATE,
                T.REGISTERED_AGE = S.REGISTERED_AGE,
                T.PICTURE_LARGE = S.PICTURE_LARGE,
                T.PICTURE_MEDIUM = S.PICTURE_MEDIUM,
                T.PICTURE_THUMBNAIL = S.PICTURE_THUMBNAIL
            WHEN NOT MATCHED THEN INSERT (
                GENDER, EMAIL, PHONE, CELL, ID, NAT,
                NAME_TITLE, NAME_FIRST, NAME_LAST,
                LOCATION_STREET_NUMBER, LOCATION_STREET_NAME, LOCATION_CITY, LOCATION_STATE,
                LOCATION_COUNTRY, LOCATION_POSTCODE,
                LOCATION_COORDINATES_LATITUDE, LOCATION_COORDINATES_LONGITUDE,
                LOCATION_TIMEZONE_OFFSET, LOCATION_TIMEZONE_DESCRIPTION,
                LOGIN_UUID, LOGIN_USERNAME, LOGIN_PASSWORD, LOGIN_SALT, LOGIN_MD5, LOGIN_SHA1, LOGIN_SHA256,
                DOB_DATE, DOB_AGE,
                REGISTERED_DATE, REGISTERED_AGE,
                PICTURE_LARGE, PICTURE_MEDIUM, PICTURE_THUMBNAIL
            ) VALUES (
                S.GENDER, S.EMAIL, S.PHONE, S.CELL, S.ID, S.NAT,
                S.NAME_TITLE, S.NAME_FIRST, S.NAME_LAST,
                S.LOCATION_STREET_NUMBER, S.LOCATION_STREET_NAME, S.LOCATION_CITY, S.LOCATION_STATE,
                S.LOCATION_COUNTRY, S.LOCATION_POSTCODE,
                S.LOCATION_COORDINATES_LATITUDE, S.LOCATION_COORDINATES_LONGITUDE,
                S.LOCATION_TIMEZONE_OFFSET, S.LOCATION_TIMEZONE_DESCRIPTION,
                S.LOGIN_UUID, S.LOGIN_USERNAME, S.LOGIN_PASSWORD, S.LOGIN_SALT, S.LOGIN_MD5, S.LOGIN_SHA1, S.LOGIN_SHA256,
                S.DOB_DATE, S.DOB_AGE,
                S.REGISTERED_DATE, S.REGISTERED_AGE,
                S.PICTURE_LARGE, S.PICTURE_MEDIUM, S.PICTURE_THUMBNAIL
            );
        """)
    cur.close()
    conn.close()
    print("Snowflake loading is completed.")

    
# ========== DAG Definition ==========
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id="API_s3_snowflake_load",
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    description='ETL pipeline: API → S3 → Snowflake without error handling',
    tags=['ETL', 'Airflow', 'Snowflake']
) as dag:

    task1 = PythonOperator(
        task_id='fetch_api_data',
        python_callable = fetch_and_save_api_data_csv
    )

    task2 = PythonOperator(
        task_id='upload_to_s3',
        python_callable = upload_to_s3
    )

    task3 = PythonOperator(
        task_id='load_s3_stage_target',
        python_callable = s3_snowflake_truncate_and_load
    )

    # Define task dependencies
    task1 >> task2 >> task3
