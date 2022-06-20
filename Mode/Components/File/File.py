import pygame

from Mode.Components import Component, Text


class File(Component):
    def __init__(self, state, pos, file, on_click):
        super().__init__(state, pos, (700, 40))
        self.file = file
        self.on_click = on_click

    def process_event(self, event):
        handled = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_mouse_over(event.pos):
                handled = True
                self.on_click(self.file)
        return handled

    def update(self):
        pass

    def render(self, surface):
        pygame.draw.rect(surface,
                         (0, 255, 0),
                         pygame.Rect(self.x, self.y, self.width, self.height),
                         1)
        Text(self.state, self.file['display'], 'filename_small',
             midleft=(self.x + 20, self.y + (self.height // 2)),
             ).render(surface)
