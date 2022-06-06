import pygame.draw_py


class Background:
    def __init__(self, bg_color, fg_color, grid_size):
        super().__init__()
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.grid_size = grid_size
        self.offset = 0
        self.tick = 0

    def process_event(self, event):
        pass

    def update(self, state):
        self.tick += 1
        if self.tick > 3:
            self.tick = 0
            self.offset += 1
            if self.offset >= self.grid_size:
                self.offset = 0

    def grid_step(self, start, end, step):
        while start <= end:
            yield start
            start += step

    def render(self, surface):
        surface.fill(self.bg_color)
        for x in self.grid_step(0, surface.get_width(), self.grid_size):
            x = x + self.offset
            pygame.draw_py.draw_line(surface, self.fg_color, (x, 0), (x, surface.get_height()), 1)

        for y in self.grid_step(0, surface.get_height(), self.grid_size):
            y = y + self.offset
            pygame.draw_py.draw_line(surface, self.fg_color, (0, y), (surface.get_width(), y), 1)
