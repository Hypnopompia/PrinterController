import pygame


class ProgressBar:
    def __init__(self, state, pos, size):
        self.state = state
        self.progress = 0
        self.x, self.y = self.pos = pos
        self.width, self.height = self.size = size

    def set_progress(self, progress: int):
        if progress > 0:
            self.progress = progress / 100

    def process_event(self, event):
        pass

    def update(self):
        pass

    def render(self, surface):
        width = int(self.width * self.progress)
        pygame.draw.rect(surface, (57, 136, 207), pygame.Rect(self.x, self.y, self.width, self.height), 1)
        pygame.draw.rect(surface, (57, 136, 207), pygame.Rect(self.x, self.y, width, self.height))

