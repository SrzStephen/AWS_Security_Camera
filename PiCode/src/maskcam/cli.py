import click
from .settings import *
from pathlib import Path
from attentive import quitevent
from time import time, sleep
from json import dumps, JSONDecodeError
from dataclasses import dataclass
from typing import Generator
from .common_fns import data_generator, session_with_retry_policy, set_verbosity
from base64 import b64encode
import RPi.GPIO as GPIO
from time import time, sleep
from .settings import DOOR_OUT_PIN, DOOR_OVERRIDE_BUTTON, OPEN_TIME, DEVICE_NAME
from logging import getLogger
from .common_fns import session_with_retry_policy, open_door, get_serial_number, Pinger
from json import dumps
import atexit
import pytz
from datetime import datetime

logger = getLogger(__name__)


@atexit.register
def cleanup_GPIO_on_exit():
    logger.info("Cleaning up GPIO")
    GPIO.cleanup()


GPIO.setmode(GPIO.BOARD)


@dataclass
class ConfigObject:
    camera_num: int
    invert_cam: bool
    device_name: str
    min_diff: int
    gateway_url: str
    generator: Generator


config_class = click.make_pass_decorator(ConfigObject, ensure=True)


# todo proper knobs on some of these
@click.group()
@click.option('--camera_number', default=CAMERA_NUMBER(), help=CAMERA_NUMBER.help(), type=int)
@click.option('--camera_invert', default=INVERT_CAMERA(), help=INVERT_CAMERA.help(), type=bool)
@click.option('--device_name', default=DEVICE_NAME(), help=DEVICE_NAME.help(), type=str)
@click.option('--minimum_difference', default=MIN_PERCENTAGE_DIFF(), help=MIN_PERCENTAGE_DIFF.help(), type=int)
@click.option('--api_gateway', default=AWS_API_GATEWAY(), help=AWS_API_GATEWAY.help(), type=str)
@click.option('-v --verbose', default=1, count=True, help="Verbosity. More v, more verbose. Eg -vvv")
@click.option('--door_button', default=DOOR_OVERRIDE_BUTTON(), help=DOOR_OVERRIDE_BUTTON.help())
@click.option('--door_pin', default=DOOR_OUT_PIN(), help=DOOR_OUT_PIN.help())
@config_class
def cli(config, camera_number, camera_invert, device_name, minimum_difference, api_gateway, verbose):
    GPIO.setup(DOOR_OVERRIDE_BUTTON(), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DOOR_OUT_PIN(), GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)

    # Trigger door open when we hit the door override button
    # Doing this to pass some params into the function
    callback_fn = lambda x: open_door(door_pin, api_gateway, open_time, device_name)
    GPIO.add_event_detect(DOOR_OVERRIDE_BUTTON(), GPIO.RISING, callback=callback_fn)

    # setup logging
    set_verbosity(verbose)
    # Set up lazy loading for image generator
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
    file_path = Path(file_path)
    # record data to check, debugging command, does not put anything to aws
    start = time()
    while not quitevent.is_set():
        if file_path.is_file():
            raise FileExistsError(f"Inputted directory {file_path.abs()} is a file")
        for CameraObject, image in config.generator:
            if not file_path.exists():
                file_path.mkdir(parents=True)


@cli.command("to_aws")
@config_class
def to_aws(config):
    serial = get_serial_number()
    ping = Pinger(gateway_URL=f"{config.gateway_url}/ping", device_name=config.device_name)
    ping.start()
    while not quitevent.is_set():
        for CameraObject, image in config.generator:
            # We got an event where the camera was diffed.
            with session_with_retry_policy() as Session:
                # Not strictly correct, not a binary image.
                data = dict(photo_data=b64encode(image),
                            timestamp=datetime.utcnow().replace(tzinfo=pytz.utc).isoformat(), device_name=DEVICE_NAME(),
                            person_threshhold=PERSON_PERCENTAGE(), mask_treshhold=1 - NO_MASK_THRESHOLD(),
                            device_serial=serial)
                response = Session.post(f"{config.gateway_url}/classify", data=dumps(data))
                try:
                    response.raise_for_status()
                except Exception as e:
                    # If we get a non 200 status code, try again
                    logger.debug(e)
                    logger.warning(f"got {response.status_code} \n for payload {data} \n with data {response.content}")
                    continue
                try:
                    response = response.json()
                except JSONDecodeError:
                    logger.warning(f"Invalid JSON response from classify \n {response.content}")
                    continue
                # response will look like something in responses.py in test_stubs
                # For this to turn on, everyone in the frame _MUST_ have a mask threshold
                if len(response) > 0:
                    detections_list = []
                    for detection in response:
                        # Check that it's detected a person
                        if detection['name'] == "person":
                            # Check that we're sure its a person
                            if detection['percentage_probability'] > PERSON_PERCENTAGE():
                                mask_detection = 1 - detection['classes']['no_mask']
                                if mask_detection > NO_MASK_THRESHOLD():
                                    detections_list.append(mask_detection)
                    # If all the dections were positive then open door
                    if len(detections_list) == len(response):
                        open_door()
                    else:
                        logger.info(f"{len(response) - len(detections_list)} person in frame wasn't wearing a mask."
                                    f"Not opening door")
