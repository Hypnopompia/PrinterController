import pygame


class TextComponent:
    def __init__(self, state, pos, width, text, font="small", color="text_light", align="left", highlight=False):
        self.text_x = None
        self.state = state
        self.x, self.y = self.pos = pos
        self.width = width
        self.text_width = self.width
        self.text = text
        self.font = font
        self.align = align
        self.highlight = highlight
        self.surface = None
        self.color = color

    def process_event(self, event):
        pass

    def update(self):
        pass

    def set_text(self, text):
        if text != self.text:
            self.text = text
            self.surface = None

    def make_surface(self):
        offset = 1
        if self.font == "medium":
            offset = 2
        if self.font == "large":
            offset = 3
        text = self.state.fonts[self.font].render(self.text, True, self.state.colors[self.color])
        highlight = self.state.fonts[self.font].render(self.text, True, self.state.colors[self.color + "_highlight"])

        self.surface = pygame.Surface((text.get_width() + offset, text.get_height() + offset), pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()
        self.surface.blit(highlight, (offset, offset))
        self.surface.blit(text, (0, 0))

        self.text_width = self.surface.get_width()

        if self.align == "left":
            self.text_x = self.x
        if self.align == "center":
            self.text_x = (self.width // 2) - (self.text_width // 2)
        elif self.align == "right":
            self.text_x = self.width - self.text_width

    def render(self, surface):
        if self.surface is None:
            self.make_surface()

        # pygame.draw.rect(surface, self.state.colors['border'], pygame.Rect(self.x, self.y, self.width, self.surface.get_height()), 1)
        # pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(self.x + self.text_x, self.y, self.surface.get_width(), self.surface.get_height()), 1)

        surface.blit(self.surface, (self.x + self.text_x, self.y))
