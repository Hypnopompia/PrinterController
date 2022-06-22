import pygame.draw

from Mode.Mode import Mode
from .Components import Background, Text, Hud, Button, Temperature


class LevelMode(Mode):
    def __init__(self, state, printer):
        super().__init__(state, printer)

        self.bed_x, self.bed_y = self.bed_pos = (20, 80)
        self.bed_size = (380, 380)

        self.north_west = (self.bed_x + 20, self.bed_y + 20)
        self.north_east = (self.bed_x + 260, self.bed_y + 20)
        self.center = (self.bed_x + 140, self.bed_y + 140)
        self.south_west = (self.bed_x + 20, self.bed_y + 260)
        self.south_east = (self.bed_x + 260, self.bed_y + 260)

        self.components = {
            "heading": Text(self.state, "Level Bed", "heading", center=(self.state.window_width // 2, 30)),
            "hud": Hud(self.state),
            "btn_back": Button(self.state, (680, 1), (100, 40), "Back", self.button_back_on_click),

            "btn_north_west": Button(self.state, self.north_west, (100, 100), "", self.button_north_west_on_click,
                                     color=self.state.colors['level_btn_border']),
            "btn_north_east": Button(self.state, self.north_east, (100, 100), "", self.button_north_east_on_click,
                                     color=self.state.colors['level_btn_border']),

            "btn_center": Button(self.state, self.center, (100, 100), "", self.button_center_on_click,
                                 color=self.state.colors['level_btn_border']),

            "btn_south_west": Button(self.state, self.south_west, (100, 100), "", self.button_south_west_on_click,
                                     color=self.state.colors['level_btn_border']),
            "btn_south_east": Button(self.state, self.south_east, (100, 100), "", self.button_south_east_on_click,
                                     color=self.state.colors['level_btn_border']),

            "bed_temp": Temperature(self.state, (420, 180), (360, 40), 'bed', self.toggle_bed_target_temp),
            "tool_temp": Temperature(self.state, (420, 280), (360, 40), 'tool', self.toggle_tool_target_temp),

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
        pygame.draw.rect(surface, self.state.colors['level_bed_border'],
                         (self.bed_x, self.bed_y, self.bed_size[0], self.bed_size[1]), 2);

        if self.head_pos is not None:
            pygame.draw.rect(surface, self.state.colors['level_target'],
                             (self.head_pos[0] + 10, self.head_pos[1] + 10, 80, 80))

        for component in self.components:
            self.components[component].render(surface)
