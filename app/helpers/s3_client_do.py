import os

import boto3

session = boto3.session.Session()

s3_client = session.client(
    's3',
    region_name='nyc3',
    endpoint_url=os.getenv("DIGITAL_OCEAN_ORIGIN"),
    aws_access_key_id=os.getenv("DIGITAL_OCEAN_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("DIGITAL_OCEAN_SECRET_KEY")
)
