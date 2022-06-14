import pygame
import pytweening as tween

from Mode.Mode import Mode
from .Components import Background, Button, Hud, Camera, PrintProgressBar, TextComponent, Temperature


class ControlMode(Mode):
    def __init__(self, state, printer):
        super().__init__(state, printer)

        self.background = Background(self.state)  # Dark purple
        self.title = TextComponent(self.state,
                                   pos=(0, 0),
                                   size=(self.state.window_width, 60),
                                   text="Ender 3 v2",
                                   font='large',
                                   color="text",
                                   align="center",
                                   valign="middle",
                                   highlight=True)
        self.hud = Hud(self.state)
        # self.camera = Camera(self.state, (450, 100), (300, 300), self.state.camera_source)

        self.button_home = Button(self.state, (100, 200), (160, 50), "Home", self.state.fonts['large'], (57, 136, 207),
                                  (84, 243, 255),
                                  self.button_home_on_click)
        self.button_quit = Button(self.state, (690, 20), (90, 35), "Quit", self.state.fonts['medium'], (57, 136, 207),
                                  (84, 243, 255),
                                  self.button_quit_on_click)

        self.tool_temp = Temperature(self.state, (480, 80), (160, 260), 'tool')
        self.bed_temp = Temperature(self.state, (640, 80), (160, 260), 'bed')

        self.print_progress_bar = PrintProgressBar(self.state, (20, 400), (self.state.window_width - 40, 40))

        self.components = []
        self.components.append(self.background)
        # self.components.append(self.title)
        self.components.append(self.hud)
        self.components.append(self.tool_temp)
        self.components.append(self.bed_temp)
        # self.components.append(self.print_progress_bar)
        # self.components.append(self.camera)
        # self.components.append(self.button_home)
        self.components.append(self.button_quit)

        self.camera_direction = False

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
