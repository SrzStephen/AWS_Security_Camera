import requests
from base64 import b64encode
from datetime import datetime
from json import dumps
if __name__ == "__main__":
    with open('data/test.mjpeg') as fp:
        image_data = fp.read()
    image_data = b64encode(image_data)
    data = dict(
        image=image_data,
        device_name='foo_bar_baz',
        timestamp=datetime.now().timestamp()
        )
    response = requests.post("http://localhost:3000/uploadvideo", data=dumps(data))
    response.raise_for_status()
