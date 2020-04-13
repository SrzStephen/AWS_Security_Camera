import requests
from base64 import b64encode
from datetime import datetime
from json import dumps
from pathlib import Path
import uuid
import pytz
from random import randint

GATEWAY_URL = "http://localhost:8888/upload"

if __name__ == "__main__":
    with Path('data') as datapath:
        files = datapath.glob('*.jpeg')
        for file in files:
            if randint(0, 10) == 1:
                override = "True"
            else:
                override = "False"
            myid = str(uuid.uuid4())
            with open(file.absolute(), 'rb') as fp:
                image = b64encode(fp.read()).decode('utf-8')
            data = dict(device_name="ICU_Camera",
                        timestamp=datetime.utcnow().replace(tzinfo=pytz.utc).isoformat(),
                        photo_data=image, person_threshold=0.5,
                        mask_threshold=0.5,
                        override=override)

            response = requests.post(GATEWAY_URL, data=dumps(data))
            response.raise_for_status()
