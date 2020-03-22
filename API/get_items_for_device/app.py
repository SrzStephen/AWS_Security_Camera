import json
import boto3
from logging import getLogger, INFO
from os import getenv
from uuid import uuid4
from json import loads, JSONDecodeError
from base64 import b64decode

logger = getLogger(__name__)
logger.setLevel(INFO)

aws_region = getenv("AWS_REGION")
table_name = getenv("TABLE_NAME")
dynamodb = boto3.client('dynamodb', region_name=aws_region)

def lambda_handler(event, context):
    # Someone can put in either just an id parameter, or a starting timestamp.
    pathparam = loads(event['pathParameters'])
    device_name = pathparam['id']
    from_timestamp = pathparam.get("timestamp", False)

    if from_timestamp:
        query = dict(TableName=table_name,
            KeyConditionExpression='device_name = :device_name AND timestamp > :timestamp',
            ExpressionAttributeValues = {
            ':dict': dict(S=device_name),
            ':timestamp': dict(N=from_timestamp)
        })
    else:
        query = dict(TableName=table_name,
                     Key=dict(device_name=device_name))
    response = dynamodb.get_item(query)
    return {
        "statusCode": 200,
        "body": json.dumps(response),
    }
