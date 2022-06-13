import pygame

from Mode.Components import Component, TextComponent


class Temperature(Component):
    def __init__(self, state, pos, size, temp_type):
        super().__init__(state, pos, size)
        self.target_temp_y = None
        self.target_temp_height = None
        self.target_temp = None
        self.current_temp_height = None
        self.current_temp_y = None
        self.bar_y = None
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

        self.label_text = TextComponent(
            state=self.state,
            pos=(self.x, (self.y - 35)),
            width=self.width,
            text=self.label,
            color="text",
            font="medium",
            align="center"
        )

    def process_event(self, event):
        pass

    def temp_to_height(self, temperature):
        temp_percent = (temperature - self.min_temp) / (self.max_temp - self.min_temp)
        temp_height = int(self.height * temp_percent)
        return temp_height, self.y + (self.height - temp_height)

    def update(self):
        if self.state.temps[self.temp_type]['actual'] != self.current_temp:
            self.current_temp = self.state.temps[self.temp_type]['actual']
            self.current_temp = min(self.max_temp, max(self.min_temp, self.current_temp))
            self.current_temp_height, self.current_temp_y = self.temp_to_height(self.current_temp)

        if self.state.temps[self.temp_type]['target'] != self.current_temp:
            self.target_temp = self.state.temps[self.temp_type]['target']
            self.target_temp = min(self.max_temp, max(self.min_temp, self.target_temp))
            self.target_temp_height, self.target_temp_y = self.temp_to_height(self.target_temp)

    def render(self, surface):
        pygame.draw.rect(surface, self.state.colors['infill'],
                         pygame.Rect(self.x, self.current_temp_y, self.width, self.current_temp_height)
                         )  # Infill

        pygame.draw_py.draw_line(surface, (200, 75, 75), (self.x + self.width + 2, self.target_temp_y), (self.x + self.width+7, self.target_temp_y), 5)

        pygame.draw.rect(surface, self.state.colors['border'], pygame.Rect(self.x, self.y, self.width, self.height), 2)
        self.label_text.render(surface)
