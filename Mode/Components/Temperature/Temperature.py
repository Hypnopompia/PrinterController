import pygame

from Mode.Components import Component, TextComponent


class Temperature(Component):
    def __init__(self, state, pos, size, temp_type):
        super().__init__(state, pos, size)
        self.bar_height = self.height - 40
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

        self.surface = None

        self.label_text = TextComponent(
            state=self.state,
            pos=(0, 0),
            size=(self.width, 40),
            text=self.label,
            color="text",
            font="medium",
            align="center",
            valign="middle"
        )

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
            self.surface = None

        if self.state.temps[self.temp_type]['target'] != self.target_temp:
            self.target_temp = self.state.temps[self.temp_type]['target']
            self.target_temp_height, self.target_temp_y = self.temp_to_height(
                min(self.max_temp, max(self.min_temp, self.target_temp)))
            self.surface = None

    def make_surface(self):
        self.surface = self.get_new_surface()

        pygame.draw.rect(self.surface, self.state.colors['infill'],
                         pygame.Rect(60, 40 + self.current_temp_y, 40, self.current_temp_height)
                         )  # Infill

        pygame.draw.rect(self.surface,
                         self.state.colors['border'],
                         pygame.Rect(60, 40, 40, self.height-40),
                         2)  # border

        pygame.draw_py.draw_line(self.surface,
                                 (200, 75, 75),
                                 (60, (40 + self.target_temp_y)),
                                 (60 + 40, (40 + self.target_temp_y)),
                                 5)  # target temp bar

        self.label_text.render(self.surface)  # label

    def render(self, surface):
        if self.surface is None:
            self.make_surface()

        surface.blit(self.surface, self.pos)
