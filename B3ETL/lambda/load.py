import json
import boto3

S3_LOCATION = "s3://silver-b3-api"
DATABASE_NAME = "default"
TABLE_NAME = "b3"
OUTPUT_BUCKET = "s3://bucket-miguel-output"

def lambda_handler(event, context):

    """
    AWS Lambda function handler to create an external table in Amazon Athena.

    This function creates an external table in Athena that points to data stored in an S3 bucket.
    The table schema consists of two string columns: 'rate' and 'date'.

    Parameters:
    event (dict): The event dict that contains parameters passed to the function (not used in this function)
    context (object): Runtime information provided by AWS Lambda (not used in this function)

    Returns:
    dict: A dictionary containing a status code and a success message
        {
            'statusCode': 200,
            'body': 'Success'
        }

    Side effects:
    - Creates or updates an external table in Amazon Athena
    - Stores query execution results in the specified S3 output bucket

    Dependencies:
    - boto3: AWS SDK for Python
    - Access to Amazon Athena and S3 services
    """

    create_table_query = f"""
      CREATE EXTERNAL TABLE IF NOT EXISTS {DATABASE_NAME}.{TABLE_NAME} (
          rate STRING,
          date STRING
      )
      ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
      STORED AS TEXTFILE
      LOCATION '{S3_LOCATION}'
      """

    client = boto3.client('athena')
    response = client.start_query_execution(
          QueryString=create_table_query,
          ResultConfiguration={'OutputLocation': OUTPUT_BUCKET}
      )

    return {
        'statusCode': 200,
        'body': 'Success'
    }
