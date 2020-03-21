import boto3
from .settings import AWS_REGION, MODEL_ENDPOINT_NAME, AWS_API_GATEWAY
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from requests_toolbelt import sessions

class Model():
    # Default to env var if not set
    def __init__(self, endpoint=MODEL_ENDPOINT_NAME(), aws_region=AWS_REGION()):
        self.sagemaker = boto3.client("runtime.sagemaker",
                                      region_name=aws_region)
        self.endpoint = endpoint

    def is_working(self):
        # validate that the endpoint actually works.
        # Hardcode a string and check that it works.
        raise NotImplementedError("TODO")

    def __invoke(self, payload):
        result = self.sagemaker.invoke_endpoint(
            EndpointName=MODEL_ENDPOINT_NAME(),
            ContentType=f'image/jpeg',
            body=bytearray(payload)
        )
        return result

    def has_people(self, payload):
        self.__invoke(payload)
        postprocesssing = "TODO"  # todo
        raise NotImplementedError()


class UploadTAWS():
    def __init__(self, url=AWS_API_GATEWAY()):
        retry_strategy = Retry(
            total=5,
            status_forcelist=[500, 502, 503, 504],
            method_whitelist=["POST"],
            backoff_factor=3
        )
        self.http = sessions.BaseUrlSession()
        adaptor = HTTPAdapter(max_retries=retry_strategy)
        self.http.adapters = {"https://": adaptor, "http://": adaptor}
        self.full_url = f"{AWS_API_GATEWAY()}/foo/bar"

    def send_video(self, url, payload):
        #Todo define gateway schema
        self.http.post(url, payload).raise_for_status()
        return NotImplementedError


