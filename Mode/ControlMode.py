import pygame
import pytweening as tween

from Mode.Mode import Mode
from .Components import Background
from .Components import Hud
from .Components import Camera


class ControlMode(Mode):
    def __init__(self, state):
        super().__init__(state)

        self.background = Background((60, 0, 0))
        self.hud = Hud()
        self.camera = Camera(50, 50, 200, 200, self.state.camera_source)
        self.camera_direction = False

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.printer_command("preheat")
            elif event.key == pygame.K_h:
                self.printer_command("home")

    def update(self, state):
        self.state = state
        self.hud.update(self.state)

        if self.camera:
            if not self.camera.is_moving():
                if self.camera_direction:
                    self.camera_direction = False
                    self.camera.move_to(400, 200, 2, 2, tween.easeInOutQuint, tween.easeInOutQuint)
                else:
                    self.camera_direction = True
                    self.camera.move_to(50, 50, 2, 2, tween.easeInOutQuint, tween.easeInOutQuint)

            self.camera.update(self.state)

    def render(self, surface):
        self.background.render(surface)
        self.hud.render(surface)

        if self.camera:
            self.camera.render(surface)

        text = self.state.large_font.render("Control", True, pygame.Color("orange"))
        surface_w, surface_h = surface.get_size()
        text_w, text_h = text.get_size()
        x = (surface_w // 2) - (text_w // 2)

        surface.blit(text, (x, 10))
