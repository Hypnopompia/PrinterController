import pygame


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
        self.tool_temp = "           Tool Temp: " + str(self.state.tool_temp) + "ºC / " + str(
            self.state.tool_target_temp) + "ºC"
        self.bed_temp = "            Bed Temp:  " + str(self.state.bed_temp) + "ºC /  " + str(
            self.state.bed_target_temp) + "ºC"
        self.status = "              Status: " + str(self.state.status_text)
        self.file = "                File: " + str(self.state.filename)
        self.est_print_time = "Estimated Print Time: " + self.state.get_est_print_time()
        self.print_time = "          Print Time: " + self.state.get_print_time()
        self.print_time_left = "     Print Time Left: " + self.state.get_print_time_left()
        self.z_index = "             Z-Index: " + str(self.state.current_z)

    def render(self, surface):
        fps_text = self.state.fonts['small_mono'].render(self.fps, True, self.state.colors['text_light'])
        surface.blit(fps_text, (5, 5))

        y = 85
        x = 20
        line_offset = 20

        status_text = self.state.fonts['small_mono'].render(self.status, True, self.state.colors['text_light'])
        surface.blit(status_text, (x, y))
        y += line_offset

        if self.state.tool_temp > 0:
            tool_temp_text = self.state.fonts['small_mono'].render(self.tool_temp, True,
                                                                   self.state.colors['text_light'])
            surface.blit(tool_temp_text, (x, y))
            y += line_offset

        if self.state.bed_temp > 0:
            bed_temp_text = self.state.fonts['small_mono'].render(self.bed_temp, True, self.state.colors['text_light'])
            surface.blit(bed_temp_text, (x, y))
            y += line_offset

        if self.state.filename != "":
            filename_text = self.state.fonts['small_mono'].render(self.file, True, self.state.colors['text_light'])
            surface.blit(filename_text, (x, y))
            y += line_offset

            est_print_time_text = self.state.fonts['small_mono'].render(self.est_print_time, True,
                                                                        self.state.colors['text_light'])
            surface.blit(est_print_time_text, (x, y))
            y += line_offset

        est_print_time_text = self.state.fonts['small_mono'].render(self.z_index, True, self.state.colors['text_light'])
        surface.blit(est_print_time_text, (x, y))
        y += line_offset
