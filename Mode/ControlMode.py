import pygame
import pytweening as tween

from Mode.Mode import Mode
from .Components import Background, Button, Hud, Camera, ProgressBar


class ControlMode(Mode):
    def __init__(self, state, printer):
        super().__init__(state, printer)

        self.background = Background(self.state, (17, 13, 40), (27, 23, 50), 20)  # Dark purple
        self.hud = Hud(self.state)
        # self.camera = Camera(self.state, (350, 100), (400, 400), self.state.camera_source)
        self.button_home = Button(self.state, (100, 200), (160, 50), "Home", self.state.fonts['large'], (57, 136, 207), (84, 243, 255),
                                  self.button_home_on_click)
        self.button_quit = Button(self.state, (100, 260), (160, 50), "Quit", self.state.fonts['large'], (57, 136, 207), (84, 243, 255),
                                  self.button_quit_on_click)

        self.progress_bar = ProgressBar(self.state, (10, 450), (self.state.window_width - 20, 20))

        self.components = []
        self.components.append(self.background)
        self.components.append(self.hud)
        self.components.append(self.progress_bar)
        # self.components.append(self.camera)
        self.components.append(self.button_home)
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
        # if self.camera:
        #     if not self.camera.is_moving():
        #         if self.camera_direction:
        #             self.camera_direction = False
        #             self.camera.move_to(400, 200, 2, 2, tween.easeInOutQuint, tween.easeInOutQuint)
        #         else:
        #             self.camera_direction = True
        #             self.camera.move_to(50, 50, 2, 2, tween.easeInOutQuint, tween.easeInOutQuint)

        for component in self.components:
            component.update()

            self.progress_bar.set_progress(self.state.print_progress)

    def render(self, surface):
        for component in self.components:
            component.render(surface)

        text = self.state.fonts["large"].render("Control", True, (57, 136, 207))
        surface_w, surface_h = surface.get_size()
        text_w, text_h = text.get_size()
        x = (surface_w // 2) - (text_w // 2)

        surface.blit(text, (x, 10))
