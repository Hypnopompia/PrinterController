import pygame.draw_py


class Background:
    def __init__(self, state):
        self.state = state
        self.bg_color = self.state.colors['background']
        self.fg_color = self.state.colors['background_line']
        self.grid_size = 20
        self.offset = 0
        self.tick = 0
        self.bg_surface = None

    def process_event(self, event):
        pass

    def update(self):
        pass

    def grid_step(self, start, end, step):
        while start <= end:
            yield start
            start += step

    def make_surface(self, size):
        self.bg_surface = pygame.Surface(size)
        self.bg_surface.fill(self.bg_color)
        for x in self.grid_step(0, self.bg_surface.get_width(), self.grid_size):
            x = x + self.offset
            pygame.draw_py.draw_line(self.bg_surface, self.fg_color, (x, 0), (x, self.bg_surface.get_height()), 1)

        for y in self.grid_step(0, self.bg_surface.get_height(), self.grid_size):
            y = y + self.offset
            pygame.draw_py.draw_line(self.bg_surface, self.fg_color, (0, y), (self.bg_surface.get_width(), y), 1)

    def render(self, surface):
        if self.bg_surface is None:
            self.make_surface(surface.get_size())

        surface.blit(self.bg_surface, (0, 0))
