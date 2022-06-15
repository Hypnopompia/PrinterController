import pygame

from Mode.Components.Text import Text


class PrintProgressBar:
    def __init__(self, state, pos, size):
        self.state = state
        self.x, self.y = self.pos = pos
        self.bar_y = self.y + 40
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
        Text(self.state, "Progress", 'label', midtop=(self.x + (self.width // 2), self.y)).render(surface)

        # Progress Bar
        width = int(self.width * (self.progress / 100))
        pygame.draw.rect(surface, self.state.colors['progress_infill'],
                         pygame.Rect(self.x, self.bar_y, width, self.height))  # Infill
        pygame.draw.rect(surface, self.state.colors['progress_border'],
                         pygame.Rect(self.x, self.bar_y, self.width, self.height),
                         2)  # Border

        progress_start_x = self.x + width - 30
        progress_end_x = progress_start_x + 60
        progress_center_x = self.x + width
        progress_y = self.bar_y + self.height

        if progress_start_x < self.x:
            progress_start_x = self.x
            progress_end_x = progress_start_x + 60
            progress_center_x = progress_start_x + 30

        if progress_end_x > self.x + self.width:
            progress_end_x = self.x + self.width
            progress_start_x = progress_end_x - 60
            progress_center_x = progress_start_x + 30

        progress_connector_x = (progress_end_x - progress_start_x) * (self.progress / 100) + progress_start_x

        pygame.draw.line(surface, self.state.colors['progress_border'], (self.x + width, self.y + self.height),
                         (self.x + width, progress_y + 5))

        pygame.draw.line(surface, self.state.colors['progress_border'], (progress_start_x, progress_y + 10),
                         (progress_end_x, progress_y + 10))

        pygame.draw.line(surface, self.state.colors['progress_border'],
                         (progress_connector_x, progress_y + 5),
                         (progress_connector_x, progress_y + 10))

        pygame.draw.line(surface, self.state.colors['progress_border'], (self.x + width, progress_y + 5),
                         (progress_connector_x, progress_y + 5))

        Text(self.state, self.percent_text, 'progress_label',
             midtop=(progress_center_x, progress_y + 10)).render(surface)

        # Print Time
        Text(self.state, self.state.get_print_time(), 'progress_label',
             topleft=(self.x + 5, self.y + 12)).render(
            surface)
        pygame.draw.line(surface, self.state.colors['progress_border'], (self.x, self.y + 40), (self.x, self.y + 10))
        pygame.draw.line(surface, self.state.colors['progress_border'], (self.x, self.y + 10),
                         (self.x + 80, self.y + 10))

        # Remaining Time
        Text(self.state, "-" + self.state.get_print_time_left(), 'progress_label',
             topright=(self.x + self.width - 2, self.y + 12)).render(surface)

        # pygame.draw.line(surface, self.state.colors['progress_border'], (self.x + self.width, self.y),
        #                  (self.x + self.width, self.y))
        pygame.draw.line(surface, self.state.colors['progress_border'], (self.x + self.width - 1, self.y + 40),
                         (self.x + self.width - 1, self.y + 10))
        pygame.draw.line(surface, self.state.colors['progress_border'], (self.x + self.width - 1, self.y + 10),
                         (self.x + self.width - 80 - 1, self.y + 10))
