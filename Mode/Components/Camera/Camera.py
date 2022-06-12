import time

import pygame

from .ThreadedCamera import ThreadedCamera
from .. import Component


class Camera(Component):
    def __init__(self, state, pos, size, source):
        super().__init__(state, pos, size)
        self.videoStream = ThreadedCamera(source)
        self.video_surface = None
        self.last_grab_time = 0

    def process_event(self, event):
        pass

    def update(self):
        # self.animate()
        if time.process_time() > (self.last_grab_time + 0.05):
            self.last_grab_time = time.process_time()
            self.video_surface = self.videoStream.grab_surface()

            if self.video_surface is not None:
                self.video_surface = self.aspect_scale(self.video_surface, self.width, self.height)
                self.width, self.height = self.video_surface.get_size()

    def render(self, surface):
        if self.video_surface is not None:
            surface.blit(self.video_surface, (self.x, self.y))
            pygame.draw.rect(surface, self.state.colors['border'], pygame.Rect(self.x, self.y, self.width, self.height), 2)  # Border
