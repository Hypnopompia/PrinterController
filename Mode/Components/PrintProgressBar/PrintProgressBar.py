import pygame

from Mode.Components.TextComponent import TextComponent


class PrintProgressBar:
    def __init__(self, state, pos, size):
        self.state = state
        self.progress = 0
        self.x, self.y = self.pos = pos
        self.width, self.height = self.size = size

        self.percent_text = None
        self.percent_text_surface = None
        self.progress_bar_surface = None

        self.elapsed_time = 0
        self.elapsed_time_surface = None

        self.remaining_time = 0
        self.remaining_time_surface = None

        self.set_progress(0)

    def set_progress(self, progress):
        if progress is None:
            progress = 0

        if self.progress != progress:
            self.progress = progress
            # redraw the progress bar surface here

        if self.percent_text != str(int(self.progress)) + "%":
            self.percent_text = str(int(self.progress)) + "%"
            self.percent_text_surface = TextComponent(state=self.state,
                                                                    pos=(self.x, self.y + self.height),
                                                                    width=self.width,
                                                                    text=self.percent_text,
                                                                    font="medium_mono",
                                                                    align="center")

    def set_elapsed_time(self, elapsed_time):
        if elapsed_time is None:
            self.elapsed_time = 0

        if self.elapsed_time != elapsed_time:
            self.elapsed_time = elapsed_time
            self.elapsed_time_surface = TextComponent(state=self.state,
                                                                    pos=(self.x + 10, self.y + self.height),
                                                                    width=200,
                                                                    text=self.state.get_print_time(),
                                                                    font="medium_mono")

    def set_remaining_time(self, remaining_time):
        if remaining_time is None:
            self.remaining_time = 0

        if self.remaining_time != remaining_time:
            self.remaining_time = remaining_time
            self.remaining_time_surface = TextComponent(state=self.state,
                                                                      pos=(
                                                                          self.x + self.width - 210,
                                                                          self.y + self.height),
                                                                      width=200,
                                                                      text="-" + self.state.get_print_time_left(),
                                                                      font="medium_mono",
                                                                      align="right")

    def process_event(self, event):
        pass

    def update(self):
        self.set_progress(self.state.print_progress)
        self.set_elapsed_time(self.state.print_time)
        self.set_remaining_time(self.state.print_time_left)

    def render(self, surface):
        width = int(self.width * (self.progress / 100))

        if self.elapsed_time_surface is not None:
            self.elapsed_time_surface.render(surface)

        if self.remaining_time_surface is not None:
            self.remaining_time_surface.render(surface)

        # Progress %
        if self.percent_text_surface is not None:
            self.percent_text_surface.render(surface)

        pygame.draw.rect(surface, self.state.colors['infill'],
                         pygame.Rect(self.x, self.y, width, self.height))  # Infill
        pygame.draw.rect(surface, self.state.colors['border'], pygame.Rect(self.x, self.y, self.width, self.height),
                         2)  # Border
