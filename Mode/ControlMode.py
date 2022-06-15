import pygame
import pytweening as tween

import ptext
from Mode.Mode import Mode
from .Components import Background, Text, Hud, Button, Temperature, PrintProgressBar


class ControlMode(Mode):
    def __init__(self, state, printer):
        super().__init__(state, printer)

        self.background = Background(self.state)
        self.title = Text(self.state, "Ender 3 v2", "heading", center=(self.state.window_width // 2, 30))

        self.hud = Hud(self.state)
        # self.camera = Camera(self.state, (450, 100), (300, 300), self.state.camera_source)

        # self.button_home = Button(self.state, (100, 200), (160, 50), "Home", self.state.fonts['large'], (57, 136, 207),
        #                           (84, 243, 255),
        #                           self.button_home_on_click)
        self.button_quit = Button(self.state, (680, 20), (100, 40), "Quit", self.button_quit_on_click)

        self.bed_temp = Temperature(self.state, (20, 280), (360, 40), 'bed')
        self.tool_temp = Temperature(self.state, (400, 280), (360, 40), 'tool')
        self.print_progress_bar = PrintProgressBar(self.state, (20, 360), (self.state.window_width - 40, 40))

        self.components = []
        self.components.append(self.background)
        self.components.append(self.title)
        self.components.append(self.hud)
        self.components.append(self.bed_temp)
        self.components.append(self.tool_temp)
        self.components.append(self.print_progress_bar)
        # self.components.append(self.camera)
        # self.components.append(self.button_home)
        self.components.append(self.button_quit)

    def button_home_on_click(self):
        self.home_printer()

    def button_quit_on_click(self):
        self.quit_requested()

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.printer_command("preheat")
            elif event.key == pygame.K_h:
                self.printer_command("home")

        for component in self.components:
            component.process_event(event)

    def update(self):
        for component in self.components:
            component.update()

    def render(self, surface):
        for component in self.components:
            component.render(surface)
