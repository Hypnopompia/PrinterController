from dataclasses import dataclass, field
import datetime

import pygame.font


@dataclass
class State:
    fonts: dict = field(default_factory=dict)
    colors: dict = field(default_factory=dict)
    running: bool = True
    window_width: int = 800
    window_height: int = 480
    fps: int = 60
    current_fps: int = 0
    octoprint_host: str = "ender3.local"
    octoprint_port: int = 80
    octoprint_api_key: str = "621274A756214843BB38E6C501E7B919"
    octoprint_user: str = "thunter"
    octoprint_password: str = "nothing"
    octoprint_session: str = None
    camera_source: str = "http://ender3.local/webcam/?action=stream"
    # Printer
    status_text: str = "Initializing"
    tool_temp: int = 0
    tool_target_temp: int = 0
    bed_temp: int = 0
    bed_target_temp: int = 0
    print_progress: int = 0
    est_print_time: int = 0
    print_time: int = 0
    print_time_left: int = 0
    filename: str = ""
    current_z: int = 0

    def init_fonts(self):
        font = "./assets/fonts/recharge/recharge.ttf"
        self.fonts['small'] = pygame.font.Font(font, 14)
        self.fonts['medium'] = pygame.font.Font(font, 25)
        self.fonts['large'] = pygame.font.Font(font, 40)

        mono_font = "./assets/fonts/unispace/unispace bd.ttf"
        self.fonts['small_mono'] = pygame.font.Font(mono_font, 14)
        self.fonts['medium_mono'] = pygame.font.Font(mono_font, 25)
        self.fonts['large_mono'] = pygame.font.Font(mono_font, 40)

        self.colors['background'] = (0, 36, 57)
        self.colors['background_line'] = (0, 60, 72)
        self.colors['border'] = (120, 204, 226)
        self.colors['infill'] = (57, 136, 207)
        self.colors['text'] = (120, 204, 226)
        self.colors['text_highlight'] = (128, 128, 128)
        self.colors['text_light'] = (228, 239, 240)
        self.colors['text_light_highlight'] = (128, 128, 128)

    def get_est_print_time(self):
        return str(datetime.timedelta(seconds=self.est_print_time))

    def get_print_time(self):
        return str(datetime.timedelta(seconds=self.print_time))

    def get_print_time_left(self):
        return str(datetime.timedelta(seconds=self.print_time_left))
