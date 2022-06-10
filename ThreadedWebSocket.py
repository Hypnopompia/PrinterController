from threading import Thread
import websocket
import json


class ThreadedWebSocket():
    def __init__(self, state):
        self.progress = None
        self.state_text = None
        self.state = state
        self.ws = websocket.WebSocketApp("ws://" + self.state.octoprint_host + "/sockjs/websocket",
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

        self.thread = Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

        self.current_tool_temp = 0
        self.current_bed_temp = 0

    def on_open(self, ws):
        pass

    def on_message(self, ws, message):
        # print(message)
        message_json = json.loads(message)
        if "connected" in message_json:
            ws.send(json.dumps({"auth": self.state.octoprint_user + ":" + self.state.octoprint_session}))
        elif "current" in message_json:
            current = message_json["current"]
            if "temps" in current and len(current["temps"]) > 0:
                temps = current["temps"][0]
                self.state.tool_temp = temps["tool0"]["actual"]
                self.state.bed_temp = temps["bed"]["actual"]
            if "state" in current:
                self.state.status_text = current["state"]["text"]
            if "progress" in current:
                self.state.print_progress = current["progress"]["completion"]

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        pass

    def run(self):
        self.ws.run_forever()

    def get_tool_temp(self):
        return self.current_tool_temp

    def get_bed_temp(self):
        return self.current_bed_temp
