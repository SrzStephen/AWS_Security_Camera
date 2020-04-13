from picamera import PiCamera
from picamera.array import PiRGBArray
import time
from threading import Thread
from attentive import quitevent
import cv2


class Camera(PiCamera):
    def __init__(self, camera_num: int, invert: bool):
        PiCamera.__init__(self, camera_num=camera_num, resolution=(1024, 1024))
        if invert:
            self.rotation = 180
        self.framerate = 32
        self.last_image = None
        self.updated = False
        self.stopped = False
        self.__capture_stream = PiRGBArray(self)
        self.__camera_thread = Thread(target=self.__update())

        # Let camera warm up
        time.sleep(1)

    def __update(self):
        # Short circuit on signal or stopped flag.
        while not quitevent.is_set() or not self.stopped:
            # video is lower quality but faster.
            for frame in self.capture_continuous(self.__capture_stream, format='bgr', use_video_port=True):
                self.last_image = frame.array
                self.updated = True

    def read_frame(self):
        # Only grab an updated frame
        while self.updated:
            self.updated = False
            return self.last_image

    def stop_polling(self):
        self.stopped = True

    def is_stopped(self):
        return not self.__camera_thread.is_alive()

    def start_polling(self):
        self.__camera_thread.start()

    def compare_frames(self, frame1, frame2):
        # convert frames to grayscale to speed up
        frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        # Todo, make sure this is % Pixels
        return cv2.absdiff(frame1_gray, frame2_gray)