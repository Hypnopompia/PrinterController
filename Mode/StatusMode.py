import pygame
from Mode.Mode import Mode
from .Components import Background, Text, Hud, Button, Temperature, PrintProgressBar, FileStatus
from .Components.Status.Status import Status


class StatusMode(Mode):
    def __init__(self, state, printer):
        super().__init__(state, printer)
        self.purge_length = 10
        self.purge_counter = 0

        self.components = {
            "background": Background(self.state),
            "heading": Text(self.state, self.state.printer_name, "heading", center=(self.state.window_width // 2, 30)),
            "hud": Hud(self.state),
            "btn_quit": Button(self.state, (740, 1), (40, 40), "X", self.button_quit_on_click),
            "btn_tools": Button(self.state, (680, 160), (80, 80), "", self.button_tools_on_click, "tools.png"),
            "file_status": FileStatus(self.state, (20, 80), self.choose_file_on_click, self.print_on_click,
                                      self.cancel_on_click),
            "status": Status(self.state, (20, 160)),
            "bed_temp": Temperature(self.state, (20, 280), (360, 40), 'bed', self.toggle_bed_target_temp),
            "tool_temp": Temperature(self.state, (400, 280), (360, 40), 'tool', self.toggle_tool_target_temp),
            "progress_bar": PrintProgressBar(self.state, (20, 360), (self.state.window_width - 40, 40))
        }

        self.components['btn_tools'].disable()

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
            self.components[component].process_event(event)

    def update(self):
        if self.state.printing:
            self.components['btn_tools'].disable()
        else:
            self.components['btn_tools'].enable()

        for component in self.components:
            self.components[component].update()

        if self.state.purging and self.state.temps['tool']['actual'] > 195 and not self.state.printer_busy:
            self.purge_counter += self.purge_length
            self.state.purge_status = "Purging (" + str(self.purge_counter) + "mm)..."
            self.printer.purge_filament(self.purge_length)

    def render(self, surface):
        for component in self.components:
            self.components[component].render(surface)
