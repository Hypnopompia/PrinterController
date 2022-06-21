import pygame.draw

from Mode.Mode import Mode
from .Components import Background, Text, Hud, Button


class LevelMode(Mode):
    def __init__(self, state, printer):
        super().__init__(state, printer)

        self.north_west = (220, 80)
        self.north_east = (480, 80)
        self.center = (350, 210)
        self.south_west = (220, 340)
        self.south_east = (480, 340)

        self.components = {
            "heading": Text(self.state, "Level Bed", "heading", center=(self.state.window_width // 2, 30)),
            "hud": Hud(self.state),
            "btn_back": Button(self.state, (680, 1), (100, 40), "Back", self.button_back_on_click),

            "btn_north_west": Button(self.state, self.north_west, (100, 100), "", self.button_north_west_on_click, color=self.state.colors['level_btn_border']),
            "btn_north_east": Button(self.state, self.north_east, (100, 100), "", self.button_north_east_on_click, color=self.state.colors['level_btn_border']),

            "btn_center": Button(self.state, self.center, (100, 100), "", self.button_center_on_click, color=self.state.colors['level_btn_border']),

            "btn_south_west": Button(self.state, self.south_west, (100, 100), "", self.button_south_west_on_click, color=self.state.colors['level_btn_border']),
            "btn_south_east": Button(self.state, self.south_east, (100, 100), "", self.button_south_east_on_click, color=self.state.colors['level_btn_border']),
        }

        self.head_pos = None
        self.printer.home(['x', 'y', 'z'])
        self.button_south_west_on_click(None)

    def button_back_on_click(self, button):
        self.switch_mode('status')

    def button_north_west_on_click(self, button):
        self.head_pos = self.north_west
        self.printer.move_to((40, 180))

    def button_north_east_on_click(self, button):
        self.head_pos = self.north_east
        self.printer.move_to((180, 180))

    def button_center_on_click(self, button):
        self.head_pos = self.center
        self.printer.move_to((110, 110))

    def button_south_west_on_click(self, button):
        self.head_pos = self.south_west
        self.printer.move_to((40, 40))

    def button_south_east_on_click(self, button):
        self.head_pos = self.south_east
        self.printer.move_to((180, 40))

    def process_event(self, event):
        for component in self.components:
            self.components[component].process_event(event)

    def update(self):
        for component in self.components:
            self.components[component].update()

    def render(self, surface):
        pygame.draw.rect(surface, self.state.colors['level_bed_border'], (200, 60, 400, 400), 2);

        if self.head_pos is not None:
            pygame.draw.rect(surface, self.state.colors['level_target'], (self.head_pos[0] + 10, self.head_pos[1] + 10, 80, 80));

        for component in self.components:
            self.components[component].render(surface)
