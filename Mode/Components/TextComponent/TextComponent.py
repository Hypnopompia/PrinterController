import pygame


class TextComponent:
    def __init__(self, state, pos, width, text, font="small", color="text_light", align="left", highlight=False):
        self.state = state
        self.x, self.y = self.pos = pos
        self.width = width
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

    def make_surface(self):
        offset = 1
        if self.font == "large":
            offset = 3
        text = self.state.fonts[self.font].render(self.text, True, self.state.colors[self.color])

        if not self.highlight:
            self.surface = text
            return

        highlight = self.state.fonts[self.font].render(self.text, True, self.state.colors[self.color + "_highlight"])

        self.surface = pygame.Surface((text.get_width() + offset, text.get_height() + offset), pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()
        self.surface.blit(highlight, (offset, offset))
        self.surface.blit(text, (0, 0))

        if self.align == "center":
            self.x = (self.width // 2) - (self.surface.get_width() // 2)

    def render(self, surface):
        if self.surface is None:
            self.make_surface()

        surface.blit(self.surface, (self.x, self.y))
