import requests
from base64 import b64encode
from datetime import datetime
from json import dumps
if __name__ == "__main__":
    with open('data/foo.jpeg','rb') as fp:
        image_data = fp.read()
    image_data = b64encode(image_data).decode('utf-8')
    data = dict(
        image="12345"
    )
    response = requests.post("https://postman-echo.com/post")
    requests.get(url="http://127.0.0.1:3000/classify")
    response = requests.post(url="http://127.0.0.1:3000/classify", data=dumps(data))
