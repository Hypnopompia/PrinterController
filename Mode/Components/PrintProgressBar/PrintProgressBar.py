import pygame

from Mode.Components.Text import Text


class PrintProgressBar:
    def __init__(self, state, pos, size):
        self.state = state
        self.x, self.y = self.pos = pos
        self.width, self.height = self.size = size

        self.progress = None
        self.percent_text = None

        self.set_progress(0)

    def set_progress(self, progress):
        if progress is None:
            progress = 0

        if self.progress != progress:
            self.progress = progress

            if self.percent_text != str(round(self.progress, 1)) + "%":
                self.percent_text = str(round(self.progress, 1)) + "%"

    def process_event(self, event):
        pass

    def update(self):
        self.set_progress(self.state.print_progress)

    def render(self, surface):
        width = int(self.width * (self.progress / 100))
        pygame.draw.rect(surface, self.state.colors['progress_infill'],
                         pygame.Rect(self.x, self.y, width, self.height))  # Infill
        pygame.draw.rect(surface, self.state.colors['progress_border'],
                         pygame.Rect(self.x, self.y, self.width, self.height),
                         2)  # Border

        Text(self.state, self.percent_text, 'progress_label',
             midtop=(self.x + (self.width // 2), self.y + self.height)).render(surface)
        Text(self.state, self.state.get_print_time(), 'progress_label', topleft=(self.x, self.y + self.height)).render(
            surface)
        Text(self.state, self.state.get_print_time_left(), 'progress_label',
             topright=(self.x + self.width, self.y + self.height)).render(surface)
