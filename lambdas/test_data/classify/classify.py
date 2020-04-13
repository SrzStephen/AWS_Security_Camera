import requests
from base64 import b64encode
from datetime import datetime
from json import dumps
from pathlib import Path
import uuid
import pytz
from random import randint

GATEWAY_URL = ""

if __name__ == "__main__":
    with Path('data') as datapath:
        files = datapath.glob('*.jpeg')
        for file in files:
            if randint(0, 10) == 1:
                override = True
            else:
                override = False

            with open(file.absolute(), 'rb') as fp:
                image = b64encode(fp.read())
            data = dict(id=uuid.uuid4(), device_name="ICU_Camera",
                        timestamp=datetime.utcnow().replace(tzinfo=pytz.utc).isoformat(),
                        photo_data=image, person_threshold=0.5,
                        mask_treshhold=0.5,
                        override=override)
            requests.post()

    with open('data/penguin.png', 'rb') as fp:
        image_data = fp.read()
    image_data = b64encode(image_data).decode('utf-8')

    data = dict(image=image_data, runtime=1234, device_name="DEVICE_NAME",
                person_threshold=0.532, mask_treshhold=0.5432)
    response = requests.post(GATEWAY_URL, data=dumps(data))
    response.raise_for_status()
