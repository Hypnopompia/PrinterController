class Mode:
    def __init__(self, state, printer):
        self.__observers = []
        self.state = state
        self.printer = printer

    def add_observer(self, observer):
        self.__observers.append(observer)

    def quit_requested(self):
        for observer in self.__observers:
            observer.quit_requested()

    def printer_command(self, command):
        for observer in self.__observers:
            observer.printer_command(command)

    def process_event(self, event):
        raise NotImplementedError()

    def update(self, state):
        raise NotImplementedError()

    def render(self, window):
        raise NotImplementedError()

    def home_printer(self):
        self.printer.home(['x', 'y', 'z'])