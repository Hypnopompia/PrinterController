from threading import Thread
import websocket
import json
import time

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
        if time.process_time() > self.state.last_busy_time + 2:
            self.state.printer_busy = False

        #  print(message)
        message_json = json.loads(message)
        if "connected" in message_json:
            ws.send(json.dumps({"auth": self.state.octoprint_user + ":" + self.state.octoprint_session}))
        elif "current" in message_json:
            current = message_json["current"]
            if "temps" in current and len(current["temps"]) > 0:
                temps = current["temps"][0]
                self.state.temps['tool']['actual'] = round(temps["tool0"]["actual"], 1)
                self.state.temps['tool']['target'] = round(temps["tool0"]["target"], 1)
                self.state.temps['bed']['actual'] = round(temps["bed"]["actual"], 1)
                self.state.temps['bed']['target'] = round(temps["bed"]["target"], 1)
            if "state" in current:
                self.state.status_text = current["state"]["text"]
            if "job" in current:
                job = current["job"]
                self.state.est_print_time = int(job["estimatedPrintTime"] or 0)
                if "file" in job and "display" in job["file"]:
                    file = job["file"]
                    self.state.filename = file["display"]
            if "progress" in current:
                progress = current["progress"]
                self.state.print_progress = progress["completion"] or 0
                self.state.print_time = progress["printTime"] or 0
                self.state.print_time_left = progress["printTimeLeft"] or 0
            if "currentZ" in current:
                self.state.current_z = current["currentZ"] or 0
            if "logs" in current:
                for log in current['logs']:
                    log = log.replace("Recv: ", "").strip()
                    print(log)
                    if log.startswith("echo:busy:"):
                        self.state.make_busy()

    def on_error(self, ws, error):
        raise error

    def on_close(self, ws, close_status_code, close_msg):
        pass

    def run(self):
        self.ws.run_forever()

    def get_tool_temp(self):
        return self.current_tool_temp

    def get_bed_temp(self):
        return self.current_bed_temp
