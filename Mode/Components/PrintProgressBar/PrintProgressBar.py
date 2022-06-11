import pygame

from Mode.Components import TextComponent


class PrintProgressBar:
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
        self.set_progress(self.state.print_progress)
        pass

    def render(self, surface):
        width = int((self.width-200) * (self.progress / 100))
        y = self.y + (self.height // 2) - 7

        elapsed_time = TextComponent.TextComponent(self.state, pos=(self.x + 10, y), width=90, text=self.state.get_print_time())
        elapsed_time.render(surface)

        print_time_left = TextComponent.TextComponent(self.state, pos=(self.x + self.width - 90, y), width=90, text="-" + self.state.get_print_time_left())
        print_time_left.render(surface)

        pygame.draw.rect(surface, self.state.colors['infill'], pygame.Rect(self.x + 100, self.y, width, self.height))  # Infill
        pygame.draw.rect(surface, self.state.colors['border'], pygame.Rect(self.x + 100, self.y, self.width - 200, self.height),
                         2)  # Border

        if self.text is not None:
            text_w, text_h = self.text.get_size()
            x = (self.width // 2) - (text_w // 2)
            surface.blit(self.text, (x, self.y - 20))
