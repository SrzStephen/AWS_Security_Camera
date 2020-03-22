import click
from .settings import CAMERA_NUMBER, DEVICE_NAME, INVERT_CAMERA, MIN_PERCENTAGE_DIFF, AWS_API_GATEWAY
from logging import getLogger, WARNING, INFO
from pathlib import Path
from attentive import quitevent
from time import time, sleep
from json import dumps, JSONDecodeError
from datetime import datetime
from dataclasses import dataclass
from typing import Generator
from .common_fns import data_generator, session_with_retry_policy
from base64 import b64encode
logger = getLogger(__name__)
# shh
getLogger("PIL").setLevel(WARNING)
getLogger("boto3").setLevel(WARNING)

@dataclass
class ConfigObject:
    camera_num: int
    invert_cam: bool
    device_name: str
    min_diff: int
    gateway_url: str
    generator: Generator


config_class = click.make_pass_decorator(ConfigObject, ensure=True)


@click.group()
@click.option('--camera_number', default=CAMERA_NUMBER(), help=CAMERA_NUMBER.help(), type=int)
@click.option('--camera_invert', default=INVERT_CAMERA(), help=INVERT_CAMERA.help(), type=bool)
@click.option('--device_name', default=DEVICE_NAME(), help=DEVICE_NAME.help(), type=str)
@click.option('--minimum_difference', default=MIN_PERCENTAGE_DIFF(), help=MIN_PERCENTAGE_DIFF.help(), type=int)
@click.option('--api_gateway', default=AWS_API_GATEWAY(), help=AWS_API_GATEWAY.help(), type=str)
@config_class
def cli(config, camera_number, camera_invert, device_name, minimum_difference, api_gateway):
    gen = data_generator(cam_num=camera_number, invert=camera_invert, threshold=minimum_difference)

    config = config(camera_num=camera_number,
                    invert_cam=camera_invert,
                    device_name=device_name,
                    min_diff=minimum_difference,
                    gateway_url=api_gateway,
                    generator=gen
                    )


@cli.command("to_file")
@click.option("--file_path", default="/tmp/data", help="Directory to save predictions to", type=str)
@config_class
def to_file(config, file_path):
    # record data to check, debugging command, does not put anything to aws
    raise NotImplementedError()


@cli.command("to_aws")
@config_class
def to_aws(config):
    start = time()
    while not quitevent.is_set():
        for CameraObject, thumbnail_image in config.generator:
            # We got an event where the camera was diffed.
            with session_with_retry_policy() as Session:
                # Not strictly correct, not a binary image. TODO fix
                data = dict(image=b64encode(thumbnail_image))
                response = Session.post(f"{config.gateway_url}/classify", data=dumps(data))
                if not response.status_code == 200:
                    logger.warning(f"request to API endpoint {config.gateway_url} returned a non 200 status code")
                    continue
                try:
                    response = response.json()
                except JSONDecodeError:
                    logger.warning(f"Invalid JSON response from classify \n {response.content}")
                    continue
                # Todo, figure out response.
                num_people_in_frame = 1234
                if num_people_in_frame > 0:
                    video_byte = CameraObject.get_video()
                    data = dict(
                        device_name=config.device_name,
                        image=b64encode(thumbnail_image),
                        detected_people=num_people_in_frame,
                        timestamp=datetime.timestamp(),
                        video=b64encode(video_byte)
                    )
                    response = Session.post(f"{config.gateway_url}/uploadvideo", data=dumps(data))
                    if not response.status_code == 200:
                        logger.warning(f"request to API Endpoint foo failed.")
                        continue
                    uuid = response.json()['uuid']
                    logger.info(f"Successfully uploaded video for {uuid}")