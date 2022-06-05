import pygame
import pytweening as tween

from Mode.Mode import Mode
from .Components import Background, Button, Hud, Camera


class ControlMode(Mode):
    def __init__(self, state, printer):
        super().__init__(state, printer)

        self.background = Background((60, 0, 0))
        self.hud = Hud()
        self.camera = False  # Camera(50, 50, 200, 200, self.state.camera_source)
        self.button_home = Button(100, 100, 160, 50, "Home", self.state.large_font, pygame.Color("darkorange2"), pygame.Color("firebrick2"),
                                  self.button_home_on_click)

        self.components = []
        self.components.append(self.background)
        self.components.append(self.hud)
        # self.components.append(self.camera)
        self.components.append(self.button_home)

        self.camera_direction = False

    def button_home_on_click(self):
        self.home_printer()

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.printer_command("preheat")
            elif event.key == pygame.K_h:
                self.printer_command("home")

        for component in self.components:
            component.process_event(event)

    def update(self, state):
        self.state = state

        if self.camera:
            if not self.camera.is_moving():
                if self.camera_direction:
                    self.camera_direction = False
                    self.camera.move_to(400, 200, 2, 2, tween.easeInOutQuint, tween.easeInOutQuint)
                else:
                    self.camera_direction = True
                    self.camera.move_to(50, 50, 2, 2, tween.easeInOutQuint, tween.easeInOutQuint)

        for component in self.components:
            component.update(self.state)

    def render(self, surface):
        for component in self.components:
            component.render(surface)

        text = self.state.large_font.render("Control", True, pygame.Color("orange"))
        surface_w, surface_h = surface.get_size()
        text_w, text_h = text.get_size()
        x = (surface_w // 2) - (text_w // 2)

        surface.blit(text, (x, 10))
