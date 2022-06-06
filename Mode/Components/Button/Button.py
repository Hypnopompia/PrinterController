import pygame

from Mode.Components import Component


class Button(Component):
    def __init__(self, x, y, width, height, label, font, fg_color, bg_color, on_click):
        super().__init__(x, y, width, height)
        self.label = label
        self.font = font
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.on_click = on_click

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_mouse_over(event.pos):
                self.on_click()

    def update(self, state):
        # if self.is_mouse_over():
        #     self.current_color = self.color_hover
        pass

    def render(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.get_rect())
        text = self.font.render(self.label, True, self.fg_color)

        text_w, text_h = text.get_size()
        x = (self.width // 2) - (text_w // 2) + self.x

        surface.blit(text, (x, self.y))
