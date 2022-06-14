import pygame

from Mode.Components import Component


class TextComponent(Component):
    def __init__(self, state, pos, size, text, font="small", color="text_light", align="left", valign="top",
                 highlight=False):
        super().__init__(state, pos, size)
        self.text = text
        self.font = font
        self.align = align
        self.valign = valign
        self.highlight = highlight
        self.color = color

        self.surface = None

        self.text_x = None
        self.text_y = None
        self.text_width = self.width
        self.text_height = None

    def process_event(self, event):
        pass

    def update(self):
        pass

    def set_text(self, text):
        if text != self.text:
            self.text = text
            self.surface = None

    def make_surface(self):
        self.surface = self.get_new_surface()

        offset = 1
        if self.font == "medium":
            offset = 2
        if self.font == "large":
            offset = 3

        text_fg_surface = self.state.fonts[self.font].render(self.text, True, self.state.colors[self.color])
        text_highlight_surface = self.state.fonts[self.font].render(self.text, True, self.state.colors[self.color + "_highlight"])
        text_surface = self.get_new_surface((text_fg_surface.get_width() + offset, text_fg_surface.get_height() + offset))
        text_surface.blit(text_highlight_surface, (offset, offset))
        text_surface.blit(text_fg_surface, (0, 0))

        self.text_width = text_surface.get_width()
        self.text_height = text_surface.get_height()

        if self.align == "left":
            self.text_x = 0
        elif self.align == "center":
            self.text_x = (self.width // 2) - (self.text_width // 2)
        elif self.align == "right":
            self.text_x = self.width - self.text_width

        if self.valign == "top":
            self.text_y = 0
        elif self.valign == "middle":
            self.text_y = (self.height // 2) - (self.text_height // 2)
        elif self.valign == "bottom":
            self.text_y = self.height - self.text_height

        self.surface.blit(text_surface, (self.text_x, self.text_y))

    def render(self, surface):
        if self.surface is None:
            self.make_surface()

        # surface.blit(self.surface, (self.x, self.y))
