from dataclasses import dataclass

import pygame.font


@dataclass
class State:
    tool_temp: int
    bed_temp: int
    small_font: pygame.font
    large_font: pygame.font
    running: bool = True
    window_width: int = 800
    window_height: int = 480
    fps: int = 60
    current_fps: int = 0
    status_text: str = "Initializing"
    preheating: bool = False
    octoprint_host: str = "ender3.local"
    octoprint_port: int = 80
    octoprint_api_key: str = "621274A756214843BB38E6C501E7B919"
    octoprint_user: str = "thunter"
    octoprint_password: str = "nothing"
    octoprint_session: str = None
    camera_source: str = "http://ender3.local/webcam/?action=stream"

    def __init__(self):
        # self.small_font = pygame.font.Font("./assets/fonts/control-freak/CONTF___.ttf", 14)
        # self.large_font = pygame.font.Font("./assets/fonts/control-freak/CONTF___.ttf", 40)

        # self.small_font = pygame.font.Font("./assets/fonts/dynamic/dynamic.ttf", 14)
        # self.large_font = pygame.font.Font("./assets/fonts/dynamic/dynamic.ttf", 40)

        self.small_font = pygame.font.Font("./assets/fonts/recharge/recharge bd.ttf", 14)
        self.large_font = pygame.font.Font("./assets/fonts/recharge/recharge bd.ttf", 40)
