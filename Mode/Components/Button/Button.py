import pygame

from Mode.Components import Component


class Button(Component):
    def __init__(self, x, y, width, height, label, font, color, color_hover, on_click):
        super().__init__(x, y, width, height)
        self.current_color = None
        self.label = label
        self.font = font
        self.color = color
        self.color_hover = color_hover
        self.on_click = on_click

    def is_hover(self):
        pos = pygame.mouse.get_pos()
        if self.get_rect().collidepoint(pos):
            return True
        else:
            return False

    def process_event(self, event):
        print(event)
        print("Hover: " + "Yes" if self.is_hover() else "No")
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.get_rect().collidepoint(event.pos):
                self.on_click()

    def update(self, state):
        self.current_color = self.color
        if self.is_hover():
            self.current_color = self.color_hover

    def render(self, surface):
        pygame.draw.rect(surface, self.current_color, self.get_rect())
        text = self.font.render(self.label, True, pygame.Color("white"))

        text_w, text_h = text.get_size()
        x = (self.width // 2) - (text_w // 2) + self.x

        surface.blit(text, (x, self.y))
