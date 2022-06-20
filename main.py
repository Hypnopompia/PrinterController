from sys import platform
import pygame
from RestClient import RestClient
from ThreadedWebSocket import ThreadedWebSocket
from Mode import StatusMode, ToolMode, PurgeMode, ChangeMode
from State import State


class PrinterController:
    def __init__(self):
        self.mode = None

        pygame.init()
        self.state = State()
        self.state.init()

        self.modes = {
            'status': StatusMode,
            'tool': ToolMode,
            'purge_filament': PurgeMode,
            'change_filament': ChangeMode,
        }

        self.switch_to_mode = "status"

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
        self.switch_mode('status')

        self.state.octoprint_session = self.printer.get_session_key()
        self.printer_info = ThreadedWebSocket(self.state)

    def switch_mode(self, mode):
        self.switch_to_mode = mode

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_requested()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.quit_requested()
                    return

            if self.mode is not None:
                self.mode.process_event(event)

    def update(self):
        if self.switch_to_mode is not None:
            self.mode = self.modes[self.switch_to_mode](self.state, self.printer)
            self.mode.add_observer(self)
            self.switch_to_mode = None

        self.state.current_fps = int(self.clock.get_fps())

        if self.mode is not None:
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
