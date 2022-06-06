import pygame

from Mode.Components import Component


class Button(Component):
    def __init__(self, pos, size, label, font, fg_color, bg_color, on_click):
        super().__init__(pos, size)
        self.label = label
        self.font = font
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.button_surface = None
        self.on_click = on_click
        self.draw_button()

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_mouse_over(event.pos):
                self.on_click()

    def update(self, state):
        # if self.is_mouse_over():
        #     self.current_color = self.color_hover
        pass

    def draw_button(self):
        self.button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.button_surface = self.button_surface.convert_alpha()

        pygame.draw.rect(self.button_surface, self.bg_color, self.button_surface.get_rect(), 1)
        text = self.font.render(self.label, True, self.fg_color)

        text_w, text_h = text.get_size()
        x = (self.width // 2) - (text_w // 2)
        self.button_surface.blit(text, (x, 0))

    def render(self, surface):
        surface.blit(self.button_surface, (self.x, self.y))
