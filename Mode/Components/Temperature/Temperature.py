import pygame

from Mode.Components import Component, Text


class Temperature(Component):
    def __init__(self, state, pos, size, temp_type):
        super().__init__(state, pos, size)

        self.bar_x = self.x + 60
        self.bar_y = self.y + 40
        self.bar_height = self.height - 40

        self.target_temp_y = None
        self.target_temp_height = None
        self.target_temp = None

        self.current_temp_height = None
        self.current_temp_y = None

        self.temp_height = None
        self.temp_percent = None
        self.temp_type = temp_type

        self.min_temp = 20
        if self.temp_type == "tool":
            self.max_temp = 200
            self.label = "Tool"
        elif self.temp_type == "bed":
            self.max_temp = 60
            self.label = "Bed"
        else:
            self.max_temp = 250

        self.current_temp = self.min_temp

    def process_event(self, event):
        pass

    def temp_to_height(self, temperature):
        temp_percent = (temperature - self.min_temp) / (self.max_temp - self.min_temp)
        temp_height = int(self.bar_height * temp_percent)
        return temp_height, (self.bar_height - temp_height)

    def update(self):
        if self.state.temps[self.temp_type]['actual'] != self.current_temp:
            self.current_temp = self.state.temps[self.temp_type]['actual']
            self.current_temp_height, self.current_temp_y = self.temp_to_height(
                min(self.max_temp, max(self.min_temp, self.current_temp)))

        if self.state.temps[self.temp_type]['target'] != self.target_temp:
            self.target_temp = self.state.temps[self.temp_type]['target']
            self.target_temp_height, self.target_temp_y = self.temp_to_height(
                min(self.max_temp, max(self.min_temp, self.target_temp)))
            self.target_temp_y

    def render(self, surface):
        Text(self.state, self.label, 'label', midtop=(self.x + (self.width // 2), self.y)).render(surface)

        pygame.draw.rect(surface, self.state.colors['temperature_infill'],
                         pygame.Rect(self.bar_x, self.bar_y + self.current_temp_y, 20, self.current_temp_height)
                         )  # Infill

        pygame.draw.rect(surface,
                         self.state.colors['temperature_border'],
                         pygame.Rect(self.bar_x, self.bar_y, 20, self.bar_height),
                         2)  # border

        pygame.draw.polygon(surface, self.state.colors['temperature_infill'], [
            (self.bar_x - 1, self.bar_y + self.current_temp_y),
            (self.bar_x - 1 - 10, self.bar_y + self.current_temp_y - 5),
            (self.bar_x - 1 - 10, self.bar_y + self.current_temp_y + 5),
        ])

        Text(self.state, str(round(self.current_temp)) + "º", 'regular',
             midright=(self.bar_x - 15, self.bar_y + self.current_temp_y)).render(surface)

        # pygame.draw_py.draw_line(surface,
        #                          self.state.colors['temperature_target'],
        #                          (self.bar_x, self.bar_y + self.target_temp_y),
        #                          (self.bar_x + 40, self.bar_y + self.target_temp_y),
        #                          1)  # target temp bar

        pygame.draw.polygon(surface, self.state.colors['temperature_target'], [
            (self.bar_x + 1 + 20, self.bar_y + self.target_temp_y),
            (self.bar_x + 1 + 30, self.bar_y + self.target_temp_y - 5),
            (self.bar_x + 1 + 30, self.bar_y + self.target_temp_y + 5),
        ])

        Text(self.state, str(round(self.target_temp)) + "º", 'regular',
             midleft=(self.bar_x + 5 + 30, self.bar_y + self.target_temp_y)).render(surface)

        # self.draw_outline(surface)
