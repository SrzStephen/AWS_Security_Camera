import boto3
from os import getenv
from logging import getLogger, WARNING
from base64 import b64decode
from json import loads

logger = getLogger(__name__)
logger.setLevel(WARNING)

model_endpoint = getenv("SAGEMAKER_ENDPOINT")
aws_region = getenv("AWS_REGION")
aws_key = getenv("AWS_ACCESS_KEY_ID")
aws_secret = getenv("AWS_SESSION_TOKEN")

sagemaker = boto3.client("runtime.sagemaker",
                         region_name=aws_region)


def lambda_handler(event, context):
    body = loads(event['body'])
    try:
        image = body['image']
    except KeyError:
        raise KeyError(f"image was missing from body, got body of {event['body']}")
    #Waiting for P2 to test this...
    result = sagemaker.invoke_endpoint(
        EntrypointName=model_endpoint,
        ContentType=f'image/jpeg',
        body=bytearray(b64decode(image))
    )
    return {
        "statusCode": 200,
        "body": result['Body'].decode(),
    }
