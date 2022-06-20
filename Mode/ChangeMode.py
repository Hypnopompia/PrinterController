from Mode.Mode import Mode
from .Components import Background, Text, Hud, Button, Temperature


class ChangeMode(Mode):
    READY = 0
    HEATING = 1
    EJECTING = 2
    WAITING = 3
    PURGING = 4
    STOPPED = 5

    def __init__(self, state, printer):
        super().__init__(state, printer)

        self.components = [
            Background(self.state),
            Text(self.state, "Change Filament", "heading", center=(self.state.window_width // 2, 30)),
            Hud(self.state),
            Button(self.state, (680, 1), (100, 40), "Back", self.button_back_on_click),
            Temperature(self.state, (220, 300), (360, 40), 'tool', self.toggle_tool_target_temp),
        ]

        self.continue_button = Button(self.state, (540, 160), (180, 60), "Continue", self.button_continue_on_click)

        self.change_state = self.READY
        self.state.changing_filament = True

    def button_back_on_click(self, button):
        self.switch_mode('tool')

    def button_continue_on_click(self, button):
        if self.change_state == self.WAITING:
            self.change_state = self.PURGING
        else:
            self.change_state = self.STOPPED

    def process_event(self, event):
        for component in self.components:
            component.process_event(event)

        # This is so only one button (which are in the same location) handles a click
        self.continue_button.process_event(event)

    def update(self):
        for component in self.components:
            component.update()

        if self.change_state == self.READY:
            self.change_state = self.HEATING
            self.state.change_filament_status = "Heating up hot end..."
            self.printer.start_filament_maintenance()
        elif self.change_state == self.HEATING:
            if not self.state.printer_busy:
                self.change_state = self.EJECTING
                self.state.change_filament_status = "Ejecting filament..."
                self.printer.eject_filament(400)
        elif self.change_state == self.EJECTING:
            if not self.state.printer_busy:
                self.change_state = self.WAITING
                self.state.change_filament_status = "Load filament and press continue."
        elif self.change_state == self.PURGING:
            self.state.change_filament_status = "Purging filament"
            self.continue_button.set_label("Stop")
            if not self.state.printer_busy:
                self.printer.purge_filament(25)
        elif self.change_state == self.STOPPED:
            self.printer.end_filament_maintenance()
            self.switch_mode('status')

    def render(self, surface):
        for component in self.components:
            component.render(surface)

        if self.state.changing_filament:
            Text(self.state, "Status: " + self.state.change_filament_status, "regular_mono", topleft=(100, 180)).render(
                surface)

        if self.change_state == self.WAITING or self.change_state == self.PURGING:
            self.continue_button.render(surface)
