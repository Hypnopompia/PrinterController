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

    def update(self):
        raise NotImplementedError()

    def render(self, window):
        raise NotImplementedError()

    def home_printer(self):
        self.printer.home(['x', 'y', 'z'])

    def toggle_bed_target_temp(self):
        if self.state.temps['bed']['target'] == 0:
            self.printer.set_bed_temp(60)
        else:
            self.printer.set_bed_temp(0)

    def toggle_tool_target_temp(self):
        if self.state.temps['tool']['target'] == 0:
            self.printer.set_tool_temp(0, 200)
        else:
            self.printer.set_tool_temp(0, 0)
