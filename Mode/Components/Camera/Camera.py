import pygame

from .ThreadedCamera import ThreadedCamera
from .. import Component


class Camera(Component):
    def __init__(self, pos, size, source):
        super().__init__(pos, size)
        self.state = None
        self.videoStream = ThreadedCamera(source)

    def process_event(self, event):
        pass

    def update(self, state):
        self.state = state
        self.animate()

    def render(self, surface):
        video_surface = self.videoStream.grab_surface()

        if video_surface is not None:
            video_surface = self.aspect_scale(video_surface, self.width, self.height)
            surface.blit(video_surface, (self.x, self.y))
