import pygame.draw

from Mode.Mode import Mode
from .Components import Background, Text, Hud, Button


class LevelMode(Mode):
    def __init__(self, state, printer):
        super().__init__(state, printer)

        self.components = {
            "heading": Text(self.state, "Level Bed", "heading", center=(self.state.window_width // 2, 30)),
            "hud": Hud(self.state),
            "btn_back": Button(self.state, (680, 1), (100, 40), "Back", self.button_back_on_click),

            "btn_north_west": Button(self.state, (220, 80), (100, 100), "", self.button_north_west_on_click),
            "btn_north_east": Button(self.state, (480, 80), (100, 100), "", self.button_north_east_on_click),

            "btn_center": Button(self.state, (350, 210), (100, 100), "", self.button_center_on_click),

            "btn_south_west": Button(self.state, (220, 340), (100, 100), "", self.button_south_west_on_click),
            "btn_south_east": Button(self.state, (480, 340), (100, 100), "", self.button_south_east_on_click),
        }

        self.printer.home(['x', 'y', 'z'])

    def button_back_on_click(self, button):
        self.switch_mode('status')

    def button_north_west_on_click(self, button):
        self.printer.move_to((40, 180))

    def button_north_east_on_click(self, button):
        self.printer.move_to((180, 180))

    def button_center_on_click(self, button):
        self.printer.move_to((110, 110))

    def button_south_west_on_click(self, button):
        self.printer.move_to((40, 40))

    def button_south_east_on_click(self, button):
        self.printer.move_to((180, 40))

    def process_event(self, event):
        for component in self.components:
            self.components[component].process_event(event)

    def update(self):
        for component in self.components:
            self.components[component].update()

    def render(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), (200, 60, 400, 400), 2);
        for component in self.components:
            self.components[component].render(surface)
