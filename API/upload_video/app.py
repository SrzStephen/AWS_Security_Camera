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
bucket_name = getenv("BUCKET_NAME")
dynamodb = boto3.client('dynamodb', region_name=aws_region)
s3 = boto3.client('s3', region=aws_region)


def lambda_handler(event, context):
    try:
        body = loads(event['body'])
    except JSONDecodeError:
        raise ValueError(f"Invalid input, couldn't decode {event['body']}")

    try:
        device_name = body['device_name']
        timestamp = body['timestamp']
        image = body['image']
        detected_people = body['detected_people']
        video = body['video']

    except KeyError as e:
        raise KeyError(f"Couldn't get key {e.args[0]} from payload {body}")

    uuid = uuid4()
    # Upload screenshot preview
    s3.put_object(Bucket=bucket_name,
                  Key=f"{uuid}.jpeg",
                  Body=b64decode(image),
                  ContentType='image/jpeg')
    # Upload video
    s3.put_object(Bucket=bucket_name,
                  Key=f"{video}.mjpeg",
                  Body=b64decode(image),
                  ContentType='video/x-motion-jpeg')
    # Add entries to DynamoDB
    item = dict(timestamp=dict(N=timestamp),
                device_name=dict(S=device_name),
                image_uuid=dict(S=uuid),
                detected_people=dict(N=detected_people))

    dynamodb.put_item(
        Item=item,
        TableName=table_name
    )
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Success",
            "uuid": uuid
        }),
    }
