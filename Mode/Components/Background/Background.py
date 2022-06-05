class Background:
    def __init__(self, color):
        super().__init__()
        self.color = color

    def process_event(self, event):
        pass

    def update(self, state):
        pass

    def render(self, surface):
        surface.fill(self.color)
