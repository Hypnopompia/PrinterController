import pygame

from Mode.Components.Text import Text


class Hud:
    def __init__(self, state):
        self.z_index = None
        self.print_time_left = None
        self.print_time = None
        self.est_print_time = None
        self.file = None
        self.state = state
        self.fps = None
        self.tool_temp = None
        self.bed_temp = None
        self.status = None
        self.clock = pygame.time.Clock()

    def process_event(self, event):
        pass

    def update(self):
        self.fps = "FPS: " + str(self.state.current_fps)
        self.tool_temp = "           Tool Temp: " + str(self.state.temps['tool']['actual']) + "ºC / " + str(
            self.state.temps['tool']['target']) + "ºC"
        self.bed_temp = "            Bed Temp:  " + str(self.state.temps['bed']['actual']) + "ºC /  " + str(
            self.state.temps['bed']['target']) + "ºC"
        self.status = "              Status: " + str(self.state.status_text)
        self.file = "                File: " + str(self.state.filename)
        self.est_print_time = "Estimated Print Time: " + self.state.get_est_print_time()
        self.print_time = "          Print Time: " + self.state.get_print_time()
        self.print_time_left = "     Print Time Left: " + self.state.get_print_time_left()
        self.z_index = "             Z-Index: " + str(self.state.current_z)

    def render(self, surface):
        font = "regular_mono"
        Text(self.state, self.fps, font, topleft=(5, 5)).render(surface)

        y = 85
        x = 20
        line_offset = 20

        Text(self.state, self.status, font, topleft=(x, y)).render(surface)
        y += line_offset

        # if self.state.temps['tool']['actual'] > 0:
        #     Text(self.state, self.tool_temp, font, topleft=(x, y)).render(surface)
        #     y += line_offset
        #
        # if self.state.temps['bed']['actual'] > 0:
        #     Text(self.state, self.bed_temp, font, topleft=(x, y)).render(surface)
        #     y += line_offset

        if self.state.filename != "":
            Text(self.state, self.file, font, topleft=(x, y)).render(surface)
            y += line_offset

            Text(self.state, self.est_print_time, font, topleft=(x, y)).render(surface)
            y += line_offset

        Text(self.state, self.z_index, font, topleft=(x, y)).render(surface)
        y += line_offset

