from Mode.Mode import Mode
from .Components import Background, Text, Hud, Button


class ToolMode(Mode):
    def __init__(self, state, printer):
        super().__init__(state, printer)

        self.move_x = 460
        self.move_y = 140

        self.components = {
            "heading": Text(self.state, "Tools", "heading", center=(self.state.window_width // 2, 30)),
            "hud": Hud(self.state),
            "btn_back": Button(self.state, (680, 1), (100, 40), "Back", self.button_back_on_click),
            "btn_change_filament": Button(self.state, (40, 80), (160, 160), "Change\nFilament", self.button_change_on_click, "filament.png"),
            "btn_purge_filament": Button(self.state, (220, 80), (160, 160), "Purge\nFilament", self.button_purge_on_click, "purge.png"),

            "btn_level_bed": Button(self.state, (40, 260), (160, 160), "Level\nBed", self.button_level_on_click, "level.png"),
            # "btn_tbd": Button(self.state, (220, 260), (160, 160), "TBD", self.button_tbd_on_click),

            "btn_north": Button(self.state, (self.move_x + 80, self.move_y), (60, 60), "^", self.button_north_on_click),
            "btn_west": Button(self.state, (self.move_x, self.move_y + 80), (60, 60), "<", self.button_west_on_click),
            "btn_home": Button(self.state, (self.move_x + 80, self.move_y + 80), (60, 60), "H", self.button_home_on_click),
            "btn_east": Button(self.state, (self.move_x + 80 + 80, self.move_y + 80), (60, 60), ">", self.button_east_on_click),
            "btn_south": Button(self.state, (self.move_x + 80, self.move_y + 80 + 80), (60, 60), "v", self.button_south_on_click),

            "btn_up": Button(self.state, (self.move_x + 80 + 80 + 80, self.move_y), (60, 100), "^", self.button_up_on_click),
            "btn_down": Button(self.state, (self.move_x + 80 + 80 + 80, self.move_y + 120), (60, 100), "v", self.button_down_on_click),
        }

    def button_back_on_click(self, button):
        self.switch_mode('status')

    def button_change_on_click(self, button):
        self.switch_mode('change_filament')

    def button_purge_on_click(self, button):
        self.switch_mode('purge_filament')

    def button_level_on_click(self, button):
        pass

    def button_tbd_on_click(self, button):
        pass

    def button_north_on_click(self, button):
        self.printer.jog({'y': 10})

    def button_west_on_click(self, button):
        self.printer.jog({'x': -10})

    def button_home_on_click(self, button):
        self.printer.home(['x', 'y', 'z'])

    def button_east_on_click(self, button):
        self.printer.jog({'x': 10})

    def button_south_on_click(self, button):
        self.printer.jog({'y': -10})

    def button_up_on_click(self, button):
        self.printer.jog({'z': 5})

    def button_down_on_click(self, button):
        self.printer.jog({'z': -5})

    def process_event(self, event):
        for component in self.components:
            self.components[component].process_event(event)

    def update(self):
        for component in self.components:
            self.components[component].update()

    def render(self, surface):
        for component in self.components:
            self.components[component].render(surface)
