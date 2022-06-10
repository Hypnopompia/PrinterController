import pygame


class ProgressBar:
    def __init__(self, state, pos, size):
        self.text = None
        self.state = state
        self.progress = 0
        self.x, self.y = self.pos = pos
        self.width, self.height = self.size = size

    def set_progress(self, progress):
        update = False
        if progress is not None:
            if progress != self.progress:
                update = True
            self.progress = progress
            if update:
                self.text = self.state.fonts['small'].render(str(int(self.progress)) + "%", True, (255, 255, 255))
        else:
            self.progress = 0

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
