import pygame


class Hud:
    def __init__(self):
        self.state = None
        self.fps = None
        self.tool_temp = None
        self.bed_temp = None
        self.status = None
        self.clock = pygame.time.Clock()

    def update(self, state):
        self.state = state
        self.fps = "FPS: " + str(self.state.current_fps)
        self.tool_temp = "Tool Temp: " + str(self.state.tool_temp) + "ºC"
        self.bed_temp = "Bed Temp: " + str(self.state.bed_temp) + "ºC"
        self.status = "Status: " + str(self.state.status_text)

    def render(self, surface):
        fps_text = self.state.small_font.render(self.fps, True, pygame.Color("white"))
        surface.blit(fps_text, (10, 10))

        status_text = self.state.small_font.render(self.status, True, pygame.Color("white"))
        surface.blit(status_text, (10, 25))

        if self.state.tool_temp > 0:
            tool_temp_text = self.state.small_font.render(self.tool_temp, True, pygame.Color("white"))
            surface.blit(tool_temp_text, (10, 40))

        if self.state.bed_temp > 0:
            bed_temp_text = self.state.small_font.render(self.bed_temp, True, pygame.Color("white"))
            surface.blit(bed_temp_text, (10, 55))


