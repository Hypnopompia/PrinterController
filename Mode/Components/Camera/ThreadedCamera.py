from threading import Thread
import cv2
import time

# https://stackoverflow.com/questions/58293187/opencv-real-time-streaming-video-capture-is-slow-how-to-drop-frames-or-get-sync
import numpy
import pygame


class ThreadedCamera(object):
    def __init__(self, source=0):
        self.capture = cv2.VideoCapture(source)

        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

        self.status = False
        self.surface = None
        self.last_frame_time = 0

    def update(self):
        while True:
            if self.capture.isOpened():
                self.capture.grab()  # grab frames and throw them away (skips any processing, so it's faster than read())

                # This decreases the displayed frame rate of the camera and does the surface processing in this thread
                if time.process_time() > (self.last_frame_time + 0.066):  # about 15fps
                    (status, video_frame) = self.capture.read()
                    if video_frame is not None:
                        self.last_frame_time = time.process_time()
                        # for some reasons the frames appeared inverted
                        video_frame = numpy.fliplr(video_frame)
                        video_frame = numpy.rot90(video_frame)

                        # The video uses BGR colors and PyGame needs RGB
                        video_frame = cv2.cvtColor(video_frame, cv2.COLOR_BGR2RGB)

                        self.surface = pygame.surfarray.make_surface(video_frame)
                        self.status = status

    def grab_surface(self):
        if self.status:
            return self.surface
        return None
