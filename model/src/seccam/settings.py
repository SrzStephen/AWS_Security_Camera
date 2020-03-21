from knobs import Knob
# Knobs are basically wrappers for os.getenvs that have some nicities


AWS_REGION = Knob(env_name="AWS_REGION",default='us-east=1',description="AWS region that your resources live in")
MODEL_ENDPOINT_NAME = Knob(env_name="AWS_MODEL_ENDPOINT_NAME",default=False,description="AWS Model endpoint for CVEDIA Human Detector")
AWS_API_GATEWAY = Knob(env_name="AWS_API_GATEWAY",default="Foo/bar/baz",description="AWS API Gateway Endpoint")