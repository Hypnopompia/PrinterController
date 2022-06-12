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
            self.text = str(int(self.progress)) + "%"

    def process_event(self, event):
        pass

    def update(self):
        self.set_progress(self.state.print_progress)
        pass

    def render(self, surface):
        width = int(self.width * (self.progress / 100))
        y = self.y + self.height

        elapsed_time = TextComponent.TextComponent(self.state, pos=(self.x + 10, y), width=200,
                                                   text=self.state.get_print_time(), font="medium")
        elapsed_time.render(surface)

        print_time_left = TextComponent.TextComponent(self.state, pos=(self.x + self.width - 210, y),
                                                      width=200, text="-" + self.state.get_print_time_left(), font="medium", align="right")
        print_time_left.render(surface)

        if self.text is not None:
            percentage = TextComponent.TextComponent(self.state, pos=(self.x, y),
                                                      width=self.width, text=self.text, font="medium", align="center")
            percentage.render(surface)

        pygame.draw.rect(surface, self.state.colors['infill'],
                         pygame.Rect(self.x, self.y, width, self.height))  # Infill
        pygame.draw.rect(surface, self.state.colors['border'], pygame.Rect(self.x, self.y, self.width, self.height),
                         2)  # Border


