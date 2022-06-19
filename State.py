import time
from dataclasses import dataclass, field
import datetime


@dataclass
class State:
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
    printing: bool = False
    cancelling: bool = False
    status_text: str = "Initializing"
    temps: dict = field(default_factory=dict)
    # tool_temp: int = 0
    # tool_target_temp: int = 0
    # bed_temp: int = 0
    # bed_target_temp: int = 0
    print_progress: int = 0
    est_print_time: int = 0
    print_time: int = 0
    print_time_left: int = 0
    filename: str = ""
    current_z: int = 0
    printer_busy = False
    last_busy_time = 0
    purging = False
    purge_status = None

    def init(self):
        font = "./assets/fonts/recharge/recharge.ttf"
        mono_font = "./assets/fonts/unispace/unispace bd.ttf"

        self.colors['background'] = (0, 36, 57)
        self.colors['background_line'] = (0, 60, 72)

        self.colors['text'] = (0, 255, 0)  # (228, 239, 240)

        self.colors['filestatus_border'] = (120, 204, 226)

        self.colors['label_text_top'] = (228, 239, 240)
        self.colors['label_text_bottom'] = (120, 204, 226)

        self.colors['button_border'] = (120, 204, 226)
        self.colors['button_border_on'] = (237, 64, 92)
        self.colors['button_text_top'] = (228, 239, 240)
        self.colors['button_text_bottom'] = (120, 204, 226)

        self.colors['temperature_text'] = (188, 198, 200)
        self.colors['temperature_infill'] = (46, 97, 150)
        self.colors['temperature_border'] = (101, 169, 240)
        self.colors['temperature_target'] = (237, 64, 92)

        self.colors['progress_infill'] = (46, 97, 150)
        self.colors['progress_border'] = (101, 169, 240)

        # self.colors['text_highlight'] = (128, 128, 128)
        # self.colors['text_light'] = (228, 239, 240)
        # self.colors['text_light_highlight'] = (128, 128, 128)

        self.temps['tool'] = {
            "actual": 0,
            "target": 0
        }

        self.temps['bed'] = {
            "actual": 0,
            "target": 0
        }

    def make_busy(self):
        self.last_busy_time = time.process_time()
        self.printer_busy = True

    def get_est_print_time(self):
        return str(datetime.timedelta(seconds=self.est_print_time))

    def get_print_time(self):
        return str(datetime.timedelta(seconds=self.print_time))

    def get_print_time_left(self):
        return str(datetime.timedelta(seconds=self.print_time_left))
