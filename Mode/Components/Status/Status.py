from Mode.Components.Text import Text


class Status:
    def __init__(self, state, pos):
        self.state = state
        self.x, self.y = self.pos = pos
        self.status = None
        self.est_print_time = None
        self.z_index = None

    def process_event(self, event):
        pass

    def update(self):
        self.status = "              Status: " + str(self.state.status_text)
        self.est_print_time = "Estimated Print Time: " + self.state.get_est_print_time()
        self.z_index = "             Z-Index: " + str(self.state.current_z)

    def render(self, surface):
        x = self.x
        y = self.y

        line_offset = 20
        font = "regular_mono"

        Text(self.state, self.status, font, topleft=(x, y)).render(surface)
        y += line_offset

        Text(self.state, self.est_print_time, font, topleft=(x, y)).render(surface)
        y += line_offset

        Text(self.state, self.z_index, font, topleft=(x, y)).render(surface)
        y += line_offset

        Text(self.state, "                Busy: " + ("Yes" if self.state.printer_busy else "No"), font, topleft=(x, y)).render(surface)
        y += line_offset
