from attentive import quitevent
from .camera import Camera
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from requests_toolbelt import sessions
from requests import Session
from numpy import array
# TODO typing
def data_generator(cam_num, invert, threshold):
    images = []
    last_image = 0
    with Camera(cam_num, invert) as Cam:
        # start getting images in a background thread
        Cam.start_polling()
        # While we don't sigkill
        while not quitevent.is_set():
            if Cam.updated:
                images[last_image] = Cam.read_frame()
                # Sanity check that we have two images.
                if len(images) > 1:
                    threshold_percentage = Cam.compare_frames(images[0], images[1])
                    if threshold_percentage > threshold:
                        yield Cam, images[last_image]
                # rotate frames
                if last_image == 0:
                    last_image = 1
                else:
                    last_image = 0

def session_with_retry_policy() -> Session:
    http = Session()
    retry_strategy = Retry(
        total=5,
        status_forcelist=[500, 502, 503, 504],
        method_whitelist=["POST"],
        backoff_factor=3
    )
    adaptor = HTTPAdapter(max_retries=retry_strategy)
    http.adapters = {"https://": adaptor, "http://": adaptor}
    return http