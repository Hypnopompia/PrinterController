from Mode.Mode import Mode
from .Components import Background, Text, Hud, Button, Temperature


class PurgeMode(Mode):
    def __init__(self, state, printer):
        super().__init__(state, printer)
        self.purge_length = 10
        self.purge_counter = 0

        self.components = [
            Background(self.state),
            Text(self.state, "Purge Filament", "heading", center=(self.state.window_width // 2, 30)),
            Hud(self.state),
            Button(self.state, (540, 160), (180, 60), "Stop", self.button_stop_on_click),
            Temperature(self.state, (220, 300), (360, 40), 'tool', self.toggle_tool_target_temp),
        ]

        self.state.purge_status = "Heating up hot end"
        self.state.purging = True
        self.printer.start_filament_maintenance()

    def button_stop_on_click(self, button):
        self.state.purge_status = "Stopping purge..."
        self.state.purging = False
        self.printer.end_filament_maintenance()
        self.switch_mode('status')

    def process_event(self, event):
        for component in self.components:
            component.process_event(event)

    def update(self):
        for component in self.components:
            component.update()

        if self.state.purging and self.state.temps['tool']['actual'] > 195 and not self.state.printer_busy:
            self.purge_counter += self.purge_length
            self.state.purge_status = "Purging (" + str(self.purge_counter) + "mm)..."
            self.printer.purge_filament(self.purge_length)

    def render(self, surface):
        for component in self.components:
            component.render(surface)

        if self.state.purging:
            Text(self.state, "Purge Status: " + self.state.purge_status, "regular_mono", topleft=(100, 180)).render(surface)
