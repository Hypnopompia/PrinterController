import pygame

from Mode.Components.Text import Text


class PrintProgressBar:
    def __init__(self, state, pos, size):
        self.state = state
        self.x, self.y = self.pos = pos
        self.width, self.height = self.size = size

        self.progress = None
        self.percent_text = None
        self.percent_text_surface = None
        self.progress_bar_surface = None

        self.elapsed_time = None
        self.elapsed_time_surface = None

        self.remaining_time = None
        self.remaining_time_surface = None

        self.set_progress(0)

    def set_progress(self, progress):
        if progress is None:
            progress = 0

        if self.progress != progress:
            self.progress = progress
            # redraw the progress bar surface here

            if self.percent_text != str(round(self.progress, 1)) + "%":
                self.percent_text = str(round(self.progress, 1)) + "%"
                self.percent_text_surface = TextComponent(
                    state=self.state,
                    pos=(self.x, self.y + self.height),
                    size=(self.width, 40),
                    text=self.percent_text,
                    font="medium_mono",
                    align="center",
                    valign="middle"
                )

    def set_elapsed_time(self, elapsed_time):
        if elapsed_time is None:
            self.elapsed_time = 0

        if self.elapsed_time != elapsed_time:
            self.elapsed_time = elapsed_time
            self.elapsed_time_surface = TextComponent(
                state=self.state,
                pos=(self.x, self.y + self.height),
                size=(self.width, 40),
                text=self.state.get_print_time(),
                font="medium_mono",
                align="left",
                valign="middle"
            )

    def set_remaining_time(self, remaining_time):
        if remaining_time is None:
            self.remaining_time = 0

        if self.remaining_time != remaining_time:

            self.remaining_time = remaining_time
            self.remaining_time_surface = TextComponent(
                state=self.state,
                pos=(self.x, self.y + self.height),
                size=(self.width, 40),
                text="-" + self.state.get_print_time_left(),
                font="medium_mono",
                align="right",
                valign="middle",
            )

    def process_event(self, event):
        pass

    def update(self):
        self.set_progress(self.state.print_progress)
        self.set_elapsed_time(self.state.print_time)
        self.set_remaining_time(self.state.print_time_left)

    def render(self, surface):
        width = int(self.width * (self.progress / 100))
        pygame.draw.rect(surface, self.state.colors['infill'],
                         pygame.Rect(self.x, self.y, width, self.height))  # Infill
        pygame.draw.rect(surface, self.state.colors['border'], pygame.Rect(self.x, self.y, self.width, self.height),
                         2)  # Border

        if self.elapsed_time_surface is not None:
            self.elapsed_time_surface.render(surface)

        if self.remaining_time_surface is not None:
            self.remaining_time_surface.render(surface)

        # Progress %
        if self.percent_text_surface is not None:
            self.percent_text_surface.render(surface)
