from dataclasses import dataclass, field
from typing import Dict

import pygame.font


@dataclass
class State:
    fonts: dict = field(default_factory=dict)
    tool_temp: int = 0
    bed_temp: int = 0
    running: bool = True
    window_width: int = 800
    window_height: int = 480
    fps: int = 60
    current_fps: int = 0
    status_text: str = "Initializing"
    print_progress: int = 0
    preheating: bool = False
    octoprint_host: str = "ender3.local"
    octoprint_port: int = 80
    octoprint_api_key: str = "621274A756214843BB38E6C501E7B919"
    octoprint_user: str = "thunter"
    octoprint_password: str = "nothing"
    octoprint_session: str = None
    camera_source: str = "http://ender3.local/webcam/?action=stream"

    def init_fonts(self):
        self.fonts['small'] = pygame.font.Font("./assets/fonts/recharge/recharge.ttf", 14)
        self.fonts['large'] = pygame.font.Font("./assets/fonts/recharge/recharge.ttf", 40)
