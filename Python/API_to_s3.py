import requests
import boto3
import pandas as pd
import io


#Step 1: Call open API
url = "https://api.freeapi.app/api/v1/public/randomusers?page=1&limit=500"
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

# AWS Credentials

aws_access_key = "xxxxxxxxxxxxxxxxx"
aws_secret_access_key = "xxxxxxxxxxxxxxxxxxxxxxxx"
region_name = "ap-south-1"

# Upload to AWS s3 bucket

bucket_name = "monalisa-123"
s3_file_name = "data/randomusers_api_data.csv "


# upload to s3

s3 = boto3.client(
    "s3",
    aws_access_key_id = aws_access_key,
    aws_secret_access_key = aws_secret_access_key,
    region_name = region_name
      )
# Upload file
s3.put_object(Bucket=bucket_name, Key=s3_file_name, Body=csv_buffer.getvalue())

 
# print(df)
# print(f"CSV file saved locally as: {csv_buffer}")
print(f"csv_buffer.getvalue() uploaded successfully to s3:{bucket_name}")
# print(f" CSV File uploaded successfully to s3:{bucket_name}")