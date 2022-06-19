import pygame

from Mode.Components import Component
from Mode.Components.Text import Text


class Button(Component):
    def __init__(self, state, pos, size, label, on_click):
        super().__init__(state, pos, size)
        self.label = label
        self.on_click = on_click
        self.draw_button()
        self.border_color = self.state.colors['button_border']

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_mouse_over(event.pos):
                self.on_click()

    def set_label(self, label):
        self.label = label

    def on(self):
        self.border_color = self.state.colors['button_border_on']

    def off(self):
        self.border_color = self.state.colors['button_border']

    def update(self):
        pass

    def draw_button(self):
        pass

    def render(self, surface):
        pygame.draw.rect(surface, self.border_color, self.get_rect(), 1)
        Text(self.state, self.label, 'button',
             center=(self.x + (self.width // 2), self.y + (self.height // 2)),
             owidth=1.5,
             ocolor="purple"
             ).render(surface)
