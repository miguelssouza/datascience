import os
from datetime import datetime
import logging
import io
import json
from json import JSONDecodeError
import pandas as pd
import boto3

TIME_STAMP = datetime.now().date()
S3_CLIENT = boto3.client('s3')
BUCKET_NAME = "brown-b3-api"
BUCKET_DESTINATION_NAME = "silver-b3-api"
FILE_NAME_PREFIX = "B3_"
FILE_NAME = f"{FILE_NAME_PREFIX}{TIME_STAMP}.json"
FILE_NAME_AFTER_HANDLING = f"{FILE_NAME}.csv"

def lambda_handler(event, context):

    """
    AWS Lambda function to transform B3 API data from JSON to CSV format.

    This function:
    1. Retrieves a JSON file from an S3 bucket.
    2. Parses the JSON data.
    3. Converts the data to a pandas DataFrame.
    4. Performs basic data transformations.
    5. Saves the transformed data as a CSV file in another S3 bucket.

    Args:
        event (dict): AWS Lambda use this parameter to pass in event data to the handler.
        context (object): AWS Lambda uses this parameter to provide runtime information to your handler.

    Returns:
        dict: A dictionary containing a status code and a message indicating success.

    Raises:
        Exception: If there's an error reading the file from S3.

    Note:
        - The function assumes the input file is in JSON format.
        - It uses global variables for S3 bucket names and file naming conventions.
        - Error handling could be improved to handle cases where 'file_body' might be unbound.
    """

    response = S3_CLIENT.get_object(Bucket='brown-b3-api', Key=FILE_NAME)

    try:
        file_body = json.loads(response['Body'].read().decode('utf-8'))
    except Exception as e:
        logging.critical(f"Read filed failed, {e}.")

    if isinstance(file_body,dict):
        df = pd.DataFrame(data=[file_body])
        df['rate'] = df.rate.str.replace(",",".")
        df['date'] = pd.to_datetime(df.date,dayfirst=True)


        csv_buffer = io.BytesIO()
        df.to_csv(csv_buffer,index=False)
        csv_buffer.seek(0)

        S3_CLIENT.upload_fileobj(csv_buffer, BUCKET_DESTINATION_NAME, FILE_NAME_AFTER_HANDLING)

    return {
        'statusCode': 200,
        'body': "Success!"
    }
