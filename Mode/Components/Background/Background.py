class Background():
    def __init__(self, color):
        super().__init__()
        self.color = color

    def render(self, surface):
        surface.fill(self.color)
