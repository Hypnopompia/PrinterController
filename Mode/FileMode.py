import math

from Mode.Mode import Mode
from .Components import Background, Text, Hud, Button, File


class FileMode(Mode):
    def __init__(self, state, printer):
        super().__init__(state, printer)

        self.components = {
            "heading": Text(self.state, "Files", "heading", center=(self.state.window_width // 2, 30)),
            "hud": Hud(self.state),
            "btn_back": Button(self.state, (680, 1), (100, 40), "Back", self.button_back_on_click),
            "btn_page_up": Button(self.state, (740, 60), (40, 80), "^", self.button_up_on_click),
            "btn_page_down": Button(self.state, (740, 380), (40, 80), "v", self.button_down_on_click),
        }

        self.file_components = []

        self.page_size = 7
        self.pages = None
        self.current_page = 1

        self.files = []
        self.load_files()
        self.load_current_page()

    def load_files(self):
        for file in self.printer.get_list_of_files('local')['files']:
            self.files.append({
                'location': file['origin'],
                'display': file['display'],
                'path': file['path'],
                'type': file['type'],
                'uploaded': file['date'],
            })

        self.files = sorted(self.files, key=lambda d: d['uploaded'], reverse=True)
        self.pages = math.ceil(len(self.files) / self.page_size)
        print("Total Pages: " + str(self.pages))

    def load_current_page(self):
        self.file_components = []
        y = 60
        start = (self.current_page * self.page_size) - self.page_size
        end = start + self.page_size
        for file in self.files[start:end]:
            self.file_components.append(File(self.state, (20, y), file, self.select_file))
            y += 60

    def button_back_on_click(self, button):
        self.switch_mode('status')

    def button_up_on_click(self, button):
        self.current_page = max(1, self.current_page - 1)
        self.load_current_page()

    def button_down_on_click(self, button):
        self.current_page = min(self.pages, self.current_page + 1)
        self.load_current_page()

    def select_file(self, file):
        self.printer.select_file(file['location'], file['path'])
        self.switch_mode('status')

    def process_event(self, event):
        for component in self.components:
            self.components[component].process_event(event)

        for component in self.file_components:
            component.process_event(event)

    def update(self):
        for component in self.components:
            self.components[component].update()

        for component in self.file_components:
            component.update()

        if self.current_page == 1:
            self.components['btn_page_up'].disable()
        else:
            self.components['btn_page_up'].enable()

        if self.current_page == self.pages:
            self.components['btn_page_down'].disable()
        else:
            self.components['btn_page_down'].enable()

    def render(self, surface):
        for component in self.components:
            self.components[component].render(surface)

        for component in self.file_components:
            component.render(surface)
