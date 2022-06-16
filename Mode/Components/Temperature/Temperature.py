import pygame

from Mode.Components import Component, Text


class Temperature(Component):
    def __init__(self, state, pos, size, temp_type, on_click):
        super().__init__(state, pos, size)

        self.on_click = on_click

        self.bar_x = self.x + 80
        self.bar_y = self.y
        self.bar_width = self.width - 80
        self.bar_height = 40

        self.target_temp_x = None
        self.target_temp_height = None
        self.target_temp = None

        self.current_temp_x = None
        self.current_temp_height = None
        self.current_temp = None

        self.temp_height = None
        self.temp_percent = None
        self.temp_type = temp_type

        self.min_temp = 27
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_mouse_over(event.pos):
                self.on_click()

    def temp_to_width(self, temperature):
        temp_percent = (temperature - self.min_temp) / (self.max_temp - self.min_temp)
        temp_width = int(self.bar_width * temp_percent)
        return temp_width

    def update(self):
        if self.state.temps[self.temp_type]['actual'] != self.current_temp:
            if self.current_temp is None:
                self.current_temp = 0
            diff = (self.state.temps[self.temp_type]['actual'] or 0) - (self.current_temp or 0)
            self.current_temp += max(-0.5, min(0.5, diff))
            self.current_temp_x = self.temp_to_width(
                min(self.max_temp, max(self.min_temp, self.current_temp)))

        if self.state.temps[self.temp_type]['target'] != self.target_temp:
            if self.target_temp is None:
                self.target_temp = 0
            diff = self.state.temps[self.temp_type]['target'] - self.target_temp
            self.target_temp += max(-0.5, min(0.5, diff))
            self.target_temp_x = self.temp_to_width(
                min(self.max_temp, max(self.min_temp, self.target_temp)))

    def render(self, surface):
        Text(self.state, self.label, 'label', midright=(self.bar_x - 5, self.y + (self.height // 2))).render(surface)

        infill_color = self.state.colors['temperature_infill'] if self.target_temp == 0 else self.state.colors[
            'temperature_target']

        pygame.draw.rect(surface, infill_color,
                         pygame.Rect(self.bar_x, self.bar_y, self.current_temp_x, self.bar_height)
                         )  # Infill

        pygame.draw.rect(surface,
                         self.state.colors['temperature_border'],
                         pygame.Rect(self.bar_x, self.bar_y, self.bar_width, self.bar_height),
                         2)  # border

        pygame.draw.polygon(surface, self.state.colors['temperature_border'], [
            (self.bar_x + self.current_temp_x, self.bar_y - 2),
            (self.bar_x + self.current_temp_x - 5, self.bar_y - 12),
            (self.bar_x + self.current_temp_x + 5, self.bar_y - 12),
        ])

        pygame.draw.lines(surface, self.state.colors['temperature_border'], False, (
            (self.bar_x + self.current_temp_x, self.bar_y),
            (self.bar_x + self.current_temp_x, self.bar_y - 20),
            (self.bar_x + self.current_temp_x - 10, self.bar_y - 20),
            (self.bar_x + self.current_temp_x - 10, self.bar_y - 10),
            (self.bar_x + self.current_temp_x - 20, self.bar_y - 10),
        ))

        Text(self.state, str(round(self.current_temp, 1)) + "º", 'regular_mono',
             midright=(self.bar_x + self.current_temp_x - 25, self.bar_y - 10),
             color=self.state.colors['temperature_text']
             ).render(surface)

        pygame.draw.polygon(surface, self.state.colors['temperature_target'], [
            (self.bar_x + self.target_temp_x, self.bar_y + self.bar_height),
            (self.bar_x + self.target_temp_x - 5, self.bar_y + self.bar_height + 10),
            (self.bar_x + self.target_temp_x + 5, self.bar_y + self.bar_height + 10),
        ])

        pygame.draw.lines(surface, self.state.colors['temperature_target'], False, (
            (self.bar_x + self.target_temp_x, self.bar_y + self.bar_height),
            (self.bar_x + self.target_temp_x, self.bar_y + self.bar_height + 20),
            (self.bar_x + self.target_temp_x - 10, self.bar_y + self.bar_height + 20),
            (self.bar_x + self.target_temp_x - 10, self.bar_y + self.bar_height + 10),
            (self.bar_x + self.target_temp_x - 20, self.bar_y + self.bar_height + 10),
        ))

        if self.target_temp == 0:
            target_temp_text = "Off"
        else:
            target_temp_text = str(round(self.target_temp, 1)) + "º"

        Text(self.state, target_temp_text, 'regular_mono',
             midright=(self.bar_x + self.target_temp_x - 25, self.bar_y + self.bar_height + 10),
             color=self.state.colors['temperature_text']
             ).render(surface)

        # self.draw_outline(surface)
