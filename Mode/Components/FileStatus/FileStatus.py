import pygame

from Mode.Components import Component, Text, Button


class FileStatus(Component):
    def __init__(self, state, pos, choose_file_on_click, print_on_click, cancel_on_click):
        self.size = (760, 60)
        super().__init__(state, pos, self.size)

        self.choose_file_on_click = choose_file_on_click
        self.print_on_click = print_on_click
        self.cancel_on_click = cancel_on_click

        self.filename = ""
        self.print_button = Button(self.state, (self.width - 100, self.y), (120, 60), "Print",
                                   self.button_print_on_click)

        self.filename_width = self.width - 140

    def button_print_on_click(self, button):
        if self.state.printing:
            self.cancel_on_click(button)
        else:
            self.print_on_click(button)

    def is_filename_clicked(self, pos):
        return pygame.Rect(self.x, self.y, self.filename_width, self.height).collidepoint(pos)

    def process_event(self, event):
        handled = self.print_button.process_event(event)

        if not handled and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_filename_clicked(event.pos):
                handled = True
                self.choose_file_on_click(self)
        return handled

    def update(self):
        self.filename = self.state.filename
        if self.state.printing:
            self.print_button.set_label("Cancel")
        else:
            self.print_button.set_label("Print")

    def render(self, surface):
        pygame.draw.rect(surface, self.state.colors['filestatus_border'],
                         pygame.Rect(self.x, self.y, self.filename_width, self.height),
                         1)  # Border

        Text(self.state, self.filename, "filename",
             center=(self.x + (self.filename_width // 2), self.y + (self.height // 2))).render(surface)

        if not self.state.cancelling:
            self.print_button.render(surface)
