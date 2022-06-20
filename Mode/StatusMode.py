import pygame
from Mode.Mode import Mode
from .Components import Background, Text, Hud, Button, Temperature, PrintProgressBar, FileStatus
from .Components.Status.Status import Status


class StatusMode(Mode):
    def __init__(self, state, printer):
        super().__init__(state, printer)
        self.purge_length = 10
        self.purge_counter = 0

        self.components = [
            Background(self.state),
            Text(self.state, self.state.printer_name, "heading", center=(self.state.window_width // 2, 30)),
            Hud(self.state),
            Button(self.state, (740, 1), (40, 40), "X", self.button_quit_on_click),
            Button(self.state, (660, 180), (120, 40), "Tools", self.button_tools_on_click),
            FileStatus(self.state, (20, 80), self.choose_file_on_click, self.print_on_click, self.cancel_on_click),
            Status(self.state, (20, 160)),
            Temperature(self.state, (20, 280), (360, 40), 'bed', self.toggle_bed_target_temp),
            Temperature(self.state, (400, 280), (360, 40), 'tool', self.toggle_tool_target_temp),
            PrintProgressBar(self.state, (20, 360), (self.state.window_width - 40, 40))
        ]

    def button_tools_on_click(self, button):
        self.switch_mode('tool')

    def button_quit_on_click(self, button):
        self.quit_requested()

    def choose_file_on_click(self):
        pass

    def print_on_click(self, button):
        self.printer.start_job()
        pass

    def cancel_on_click(self, button):
        self.printer.cancel_job()
        pass

    def process_event(self, event):
        for component in self.components:
            component.process_event(event)

    def update(self):
        for component in self.components:
            component.update()

        if self.state.purging and self.state.temps['tool']['actual'] > 190 and not self.state.printer_busy:
            self.purge_counter += self.purge_length
            self.state.purge_status = "Purging (" + str(self.purge_counter) + "mm)..."
            self.printer.purge_filament(self.purge_length)

    def render(self, surface):
        for component in self.components:
            component.render(surface)
