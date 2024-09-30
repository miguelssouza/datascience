import ssl
import boto3
from datetime import datetime
import urllib.request
import logging


B3_URL = "https://sistemaswebb3-balcao.b3.com.br/featuresDIProxy/DICall/GetRateDI/eyJsYW5ndWFnZSI6InB0LWJyIn0="
FILE_NAME_PREFIX = "B3_"
BUCKET_NAME = "brown-b3-api"
TIME_STAMP = datetime.now().date()
OBJECT_NAME = f"{FILE_NAME_PREFIX}{TIME_STAMP}.json"



def lambda_handler(event, context):

    """
    Lambda Function: B3 Data Extraction and S3 Upload

    This Lambda function extracts data from the B3 (Brasil Bolsa Balcão) API and uploads it to an S3 bucket.

    Constants:
        B3_URL (str): The URL of the B3 API endpoint.
        FILE_NAME_PREFIX (str): Prefix for the filename to be stored in S3.
        BUCKET_NAME (str): Name of the S3 bucket where the data will be stored.
        TIME_STAMP (date): Current date used in the filename.
        OBJECT_NAME (str): Full name of the object to be stored in S3.

    Function:
        lambda_handler(event, context):
            Main handler for the Lambda function.

            Args:
                event (dict): AWS Lambda uses this parameter to pass in event data to the handler.
                context (object): AWS Lambda uses this parameter to provide runtime information to your handler.

            Returns:
                dict: A dictionary containing the status code and response message.
                      {"statusCode": int, "Response": str}

            Behavior:
                1. Sets up an SSL context that doesn't verify certificates.
                2. Attempts to fetch data from the B3 API.
                3. If successful (HTTP 200), reads the response and uploads it to the specified S3 bucket.
                4. If an error occurs during the URL fetch, returns a 500 status code with the error.
                5. If successful, returns a 200 status code with a "Success" message.

    Error Handling:
        Catches urllib.error.URLError for network-related errors.

    Note:
        The function disables SSL certificate verification, which may pose security risks in a production environment.

    Dependencies:
        - ssl: For creating an SSL context
        - boto3: For interacting with AWS S3
        - datetime: For generating timestamps
        - urllib.request: For making HTTP requests
        - logging: For potential logging (currently unused in the provided code)
    """

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    response = None

    try:
        with urllib.request.urlopen(url=B3_URL,context=ctx) as response:
            if response.getcode() == 200:
                response = response.read().strip()
                s3_client = boto3.client('s3')
                response = s3_client.put_object(
                    Bucket=BUCKET_NAME,
                    Key=OBJECT_NAME,
                    Body=response
                )


    except urllib.error.URLError as e:
        return {"statusCode":500,"Response":e}

    return {"statusCode":200,"Response":"Success"}
