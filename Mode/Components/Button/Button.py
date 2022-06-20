import pygame

from Mode.Components import Component
from Mode.Components.Text import Text


class Button(Component):
    def __init__(self, state, pos, size, label, on_click, icon=None):
        super().__init__(state, pos, size)
        self.enabled = True
        self.label = label
        self.on_click = on_click
        self.border_color = self.state.colors['button_border']
        self.icon = icon

        if self.icon is not None:
            self.icon_surface = pygame.image.load("assets/images/" + self.icon)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def process_event(self, event):
        if not self.enabled:
            return False

        handled = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_mouse_over(event.pos):
                handled = True
                self.on_click(self)
        return handled

    def set_label(self, label):
        self.label = label

    def on(self):
        self.border_color = self.state.colors['button_border_on']

    def off(self):
        self.border_color = self.state.colors['button_border']

    def update(self):
        pass

    def render(self, surface):
        if not self.enabled:
            return False

        pygame.draw.rect(surface, self.border_color, self.get_rect(), 1)

        if self.icon:
            surface.blit(self.icon_surface,
                         (self.x + (self.width // 2) - (self.icon_surface.get_width() // 2), self.y))

            Text(self.state, self.label, 'button',
                 midtop=(self.x + (self.width // 2), self.y + self.icon_surface.get_height()),
                 owidth=1.5,
                 ocolor="purple"
                 ).render(surface)
        else:
            Text(self.state, self.label, 'button',
                 center=(self.x + (self.width // 2), self.y + (self.height // 2)),
                 owidth=1.5,
                 ocolor="purple"
                 ).render(surface)
