import random
import time

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

        self.rider_interval = 5
        self.rider_last_time = 0
        self.rider_speed = 10
        self.rider_tail_len = 60
        self.rider_enabled = False
        self.rider = {'axis': None, 'x': None, 'y': None, 'dir': None}
        self.rider_pos = None
        self.rider_tail_pos = None

    def process_event(self, event):
        pass

    def update(self):
        # if not self.rider_enabled:
        #     if self.rider_last_time + self.rider_interval < time.process_time():
        #         self.start_rider()
        #
        # self.update_rider()
        pass

    def start_rider(self):
        print('start')
        rider_max = {'x': self.state.window_width, 'y': self.state.window_height}

        axis = random.choice(['x', 'y'])
        move_axis = 'x' if axis == 'y' else 'y'
        self.rider['axis'] = axis
        self.rider['dir'] = random.choice([-1, 1])
        self.rider['limit'] = rider_max[move_axis]
        self.rider[axis] = random.randrange(20, rider_max[axis] - 20, 20)
        self.rider[move_axis] = 0 if self.rider['dir'] > 0 else self.rider['limit']
        self.rider_enabled = True

    def update_rider(self):
        if not self.rider_enabled:
            return

        speed = self.rider_speed * self.rider['dir']
        move_axis = 'x' if self.rider['axis'] == 'y' else 'y'

        self.rider[move_axis] += speed

        self.rider_pos = (self.rider['x'], self.rider['y'])
        tail_length = self.rider_tail_len * self.rider['dir']
        self.rider_tail_pos = (
            self.rider['x'] if move_axis == 'y' else self.rider['x'] + tail_length,
            self.rider['y'] if move_axis == 'x' else self.rider['y'] + tail_length,
        )

        if self.rider[move_axis] < 0 or self.rider[move_axis] > self.rider['limit']:
            self.reset_rider()

    def reset_rider(self):
        self.rider_enabled = False
        self.rider_last_time = time.process_time()
        self.rider = {'axis': None, 'x': None, 'y': None, 'dir': None}

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

        if self.rider_enabled:
            pygame.draw.line(surface, (75, 150, 75), self.rider_pos, self.rider_tail_pos, 2)
