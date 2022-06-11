import pygame


class Hud:
    def __init__(self, state):
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
        self.tool_temp = "Tool Temp: " + str(self.state.tool_temp) + "ºC"
        self.bed_temp = "Bed Temp: " + str(self.state.bed_temp) + "ºC"
        self.status = "Status: " + str(self.state.status_text)
        self.file = "File: " + str(self.state.filename)
        self.est_print_time = "Estimated Print Time: " + self.state.get_est_print_time()
        self.print_time = "Print Time: " + self.state.get_print_time()
        self.print_time_left = "Print Time Left: " + self.state.get_print_time_left()

    def render(self, surface):
        y = 10;

        fps_text = self.state.fonts['small'].render(self.fps, True, pygame.Color("white"))
        surface.blit(fps_text, (10, y))
        y += 15

        status_text = self.state.fonts['small'].render(self.status, True, pygame.Color("white"))
        surface.blit(status_text, (10, y))
        y += 15

        if self.state.tool_temp > 0:
            tool_temp_text = self.state.fonts['small'].render(self.tool_temp, True, pygame.Color("white"))
            surface.blit(tool_temp_text, (10, y))
            y += 15


        if self.state.bed_temp > 0:
            bed_temp_text = self.state.fonts['small'].render(self.bed_temp, True, pygame.Color("white"))
            surface.blit(bed_temp_text, (10, y))
            y += 15


        if self.state.filename != "":
            filename_text = self.state.fonts['small'].render(self.file, True, pygame.Color("white"))
            surface.blit(filename_text, (10, y))
            y += 15

        est_print_time_text = self.state.fonts['small'].render(self.est_print_time, True, pygame.Color("white"))
        surface.blit(est_print_time_text, (10, y))
        y += 15

        if self.state.print_time > 0:
            print_time_text = self.state.fonts['small'].render(self.print_time, True, pygame.Color("white"))
            surface.blit(print_time_text, (10, y))
            y += 15

        if self.state.print_time_left > 0:
            print_time_left_text = self.state.fonts['small'].render(self.print_time_left, True, pygame.Color("white"))
            surface.blit(print_time_left_text, (10, y))
            y += 15
