import pygame


class ProgressBar:
    def __init__(self, state, pos, size):
        self.text = None
        self.state = state
        self.progress = None
        self.x, self.y = self.pos = pos
        self.width, self.height = self.size = size

        self.set_progress(0)

    def set_progress(self, progress):
        if progress is None:
            progress = 0

        if progress != self.progress:
            self.progress = progress
            self.text = self.state.fonts['small'].render(str(int(self.progress)) + "%", True, (255, 255, 255))

    def process_event(self, event):
        pass

    def update(self):
        pass

    def render(self, surface):
        width = int(self.width * (self.progress / 100))
        pygame.draw.rect(surface, (57, 136, 207), pygame.Rect(self.x, self.y, self.width, self.height), 1)
        pygame.draw.rect(surface, (57, 136, 207), pygame.Rect(self.x, self.y, width, self.height))

        if self.text is not None:
            text_w, text_h = self.text.get_size()
            x = (self.width // 2) - (text_w // 2)
            surface.blit(self.text, (x, self.y - 20))
