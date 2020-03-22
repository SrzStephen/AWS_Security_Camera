from knobs import Knob
from socket import gethostname

# Knobs are basically wrappers for os.getenvs that have some niceties


CAMERA_NUMBER = Knob(env_name="CAMERA_NUMBER", default=0,
                     description="Raspberry Pi camera number according to "
                                 "https://picamera.readthedocs.io/en/release-1.13/api_camera.html#picamera")

INVERT_CAMERA = Knob(env_name="CAMERA_INVERT", default=True, description="Vertical invert camera")

DEVICE_NAME = Knob(env_name="DEVICE_NAME", default=gethostname(), description="Device Name")

AWS_REGION = Knob(env_name="AWS_REGION", default='us-east=1', description="AWS region that your resources live in")
MODEL_ENDPOINT_NAME = Knob(env_name="AWS_MODEL_ENDPOINT_NAME", default=False,
                           description="AWS Model endpoint for CVEDIA Human Detector")

AWS_API_GATEWAY = Knob(env_name="AWS_API_GATEWAY", default="Foo/bar/baz", description="AWS API Gateway Endpoint")

MIN_PERCENTAGE_DIFF = Knob(env_name="MIN_PERCENTAGE_DIFF", default=10,
                           description="Minimum difference between frames to send")
