import pygame

from Mode.Components.Text import Text


class Hud:
    def __init__(self, state):
        self.state = state
        self.fps = None

    def process_event(self, event):
        pass

    def update(self):
        self.fps = "FPS: " + str(self.state.current_fps)

    def render(self, surface):
        font = "regular_mono"
        Text(self.state, self.fps, font, topleft=(5, 5)).render(surface)
