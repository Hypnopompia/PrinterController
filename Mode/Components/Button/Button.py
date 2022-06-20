import pygame

from Mode.Components import Component
from Mode.Components.Text import Text


class Button(Component):
    def __init__(self, state, pos, size, label, on_click, icon=None):
        super().__init__(state, pos, size)
        self.label = label
        self.on_click = on_click
        self.draw_button()
        self.border_color = self.state.colors['button_border']
        self.icon = icon

        if self.icon:
            self.icon_surface = pygame.image.load("assets/images/" + self.icon)

    def process_event(self, event):
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

    def draw_button(self):
        pass

    def aspect_scale(self, img, bx, by):
        """ Scales 'img' to fit into box bx/by.
         This method will retain the original image's aspect ratio """
        ix, iy = img.get_size()
        if ix > iy:
            # fit to width
            scale_factor = bx / float(ix)
            sy = scale_factor * iy
            if sy > by:
                scale_factor = by / float(iy)
                sx = scale_factor * ix
                sy = by
            else:
                sx = bx
        else:
            # fit to height
            scale_factor = by / float(iy)
            sx = scale_factor * ix
            if sx > bx:
                scale_factor = bx / float(ix)
                sx = bx
                sy = scale_factor * iy
            else:
                sy = by

        return pygame.transform.scale(img, (int(sx), int(sy)))

    def render(self, surface):
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
