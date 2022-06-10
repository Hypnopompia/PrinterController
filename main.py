from sys import platform
import pygame
from RestClient import RestClient
from ThreadedWebSocket import ThreadedWebSocket
from Mode import ControlMode
from State import State


class PrinterController:
    def __init__(self):
        self.mode = None

        pygame.init()
        self.state = State()
        self.state.init_fonts()

        if platform == "linux" or platform == "linux2":
            # https://github.com/MobilityLab/TransitScreen/wiki/Raspberry-Pi
            self.window = pygame.display.set_mode((self.state.window_width, self.state.window_height),
                                                  pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
            # pygame.mouse.set_visible(False)
            pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
        elif platform == "darwin":
            self.window = pygame.display.set_mode((self.state.window_width, self.state.window_height),
                                                  pygame.HWSURFACE | pygame.DOUBLEBUF)

        pygame.display.set_caption('3D Printer Controller')

        self.clock = pygame.time.Clock()

        self.printer = RestClient(self.state)
        self.switch_mode(ControlMode)

        self.state.octoprint_session = self.printer.get_session_key()
        self.printer_info = ThreadedWebSocket(self.state)

    def switch_mode(self, mode):
        self.mode = mode(self.state, self.printer)
        self.mode.add_observer(self)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_requested()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.quit_requested()
                    return

            self.mode.process_event(event)

    def update(self):
        self.state.current_fps = int(self.clock.get_fps())
        self.mode.update()

    def render(self):
        if self.mode is not None:
            self.mode.render(self.window)
        pygame.display.update()

    def run(self):
        while self.state.running:
            self.process_events()
            self.update()
            self.render()
            self.clock.tick(self.state.fps)

    def quit_requested(self):
        self.state.running = False


if __name__ == '__main__':
    printerController = PrinterController()
    printerController.run()
