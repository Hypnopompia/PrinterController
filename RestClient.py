import time
import requests
import json
import logging


class RestClient:
    def __init__(self, state):
        self.session = None
        self.state = state
        self._api_key = None
        self._port = None
        self._host = None
        self._headers = None
        self._prefix = "/api"

        self.load_parameters()
        self.status = None
        self.boot()

    def get_session_key(self):
        return self.session

    def get_status(self):
        return self.status

    def load_parameters(self):
        self._host = self.state.octoprint_host
        self._port = self.state.octoprint_port
        self._api_key = self.state.octoprint_api_key
        self._headers = {'Content-Type': 'application/json', 'X-Api-Key': self._api_key}

    def boot(self):
        authenticated = False
        api_key_ok = False
        while not authenticated:
            self.status = "Logging in..."
            self.session = self.login()
            if self.session != "INVALID-SESSION":
                authenticated = True
            else:
                time.sleep(1)

        while not api_key_ok:
            self.status = "Checking API key..."
            if self.connection_ok():
                api_key_ok = True
            else:
                time.sleep(1)

        self.status = "Ready."

    def login(self):
        url = self._build_url("login")
        user = self.state.octoprint_user
        password = self.state.octoprint_password
        data = json.dumps({'user': user, 'pass': password})
        r = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
        if r.status_code == 200:
            return r.json()["session"]
        else:
            logging.warning("Authentication failed! Check username and password + CORS")
            return "INVALID-SESSION"

    def connection_ok(self):
        r = requests.get(self._build_url("version"), headers=self._headers)
        return r.status_code == 200

    def start_job(self):
        data = json.dumps({'command': 'start'})
        r = requests.post(self._build_url("job"), data=data, headers=self._headers)
        return r.status_code == 204

    def pause_job(self):
        data = json.dumps({'command': 'pause'})
        r = requests.post(self._build_url("job"), data=data, headers=self._headers)
        return r.status_code == 204

    def cancel_job(self):
        data = json.dumps({'command': 'cancel'})
        r = requests.post(self._build_url("job"), data=data, headers=self._headers)
        return r.status_code == 204

    def resume_job(self):
        data = json.dumps({'command': 'pause'})
        r = requests.post(self._build_url("job"), data=data, headers=self._headers)
        return r.status_code == 204

    def send_gcode(self, cmd):
        url = self._build_url("printer/command")
        data = json.dumps({'command': cmd})
        r = requests.post(url, data=data, headers=self._headers)
        return r.status_code == 204

    def start_filament_maintenance(self):
        self.state.make_busy()
        url = self._build_url("printer/command")
        data = json.dumps({'commands': [
            "M104 S200 T0",  # start heating hot end to 200 degrees Celsius
            "G28 X0 Y0 Z0",  # home X, Y and Z axis end-stops
            "G1 F5000",  # Set feed rate to 5000mm/m
            "G1 Z60",  # Move to 60mm Z
            "G1 X110 Y110",  # Move to middle of build plate
            "M109 S200 T0",  # Wait for T0 to reach 200 degrees before continuing with any other commands
            "M400",  # Wait for the head to stop
        ]})
        r = requests.post(url, data=data, headers=self._headers)
        return r.status_code == 204

    def eject_filament(self, length: int):
        self.state.make_busy()
        url = self._build_url("printer/command")
        data = json.dumps({'commands': [
            "G92 E0",  # zero the extruded length
            "G1 F75 E5", # push out a little bit
            "M400", # wait
            "G92, E0", # reset exturder
            "G1 F1000 E-" + str(abs(length)).strip(),  # eject filament
            "M400",  # Wait for the extruder to finish
        ]})
        r = requests.post(url, data=data, headers=self._headers)
        return r.status_code == 204

    def purge_filament(self, length: int):
        self.state.make_busy()
        url = self._build_url("printer/command")
        data = json.dumps({'commands': [
            "G92 E0",  # zero the extruded length
            "G1 F75 E" + str(abs(length)).strip(),  # extrude 10mm of feed stock
            "M400",  # Wait for the extruder to finish
        ]})
        r = requests.post(url, data=data, headers=self._headers)
        return r.status_code == 204

    def end_filament_maintenance(self):
        url = self._build_url("printer/command")
        data = json.dumps({'commands': [
            "G92 E0",  # zero the extruded length
            "G1 F75 E-1",  # retract 1mm
            "G92 E0",  # zero the extruded length
            "M104 S0 T0",  # turn off the hot end
        ]})
        r = requests.post(url, data=data, headers=self._headers)
        return r.status_code == 204

    def start_preheat(self):
        bed_temp = 60
        tool_0 = 200
        self.set_bed_temp(bed_temp)
        self.set_tool_temp(0, tool_0)

    def stop_preheat(self):
        self.set_bed_temp(0)
        self.set_tool_temp(0, 0)

    def set_bed_temp(self, temp):
        url = self._build_url("printer/bed")
        data = json.dumps({'command': 'target', 'target': int(float(temp))})
        r = requests.post(url, data=data, headers=self._headers)
        return r.status_code == 204

    def set_tool_temp(self, tool_nr, temp):
        url = self._build_url("printer/tool")
        data = json.dumps({'command': 'target', 'targets': {'tool' + str(tool_nr): int(float(temp))}})
        r = requests.post(url, data=data, headers=self._headers)
        return r.status_code == 204

    def select_file(self, filename):
        url = self._build_url("files/local/" + filename)
        data = json.dumps({'command': 'select'})
        r = requests.post(url, data=data, headers=self._headers)
        return r.status_code == 204

    # Jog the printer
    def jog(self, amount):
        data = json.dumps({'command': 'jog', **amount})
        r = requests.post(self._build_url("printer/printhead"), data=data, headers=self._headers)
        return r.status_code == 204

    # Home selected axes
    def home(self, axes):
        data = json.dumps({'command': 'home', 'axes': axes})
        r = requests.post(self._build_url("printer/printhead"), data=data, headers=self._headers)
        return r.status_code == 204

    def extrude(self, amount):
        data = json.dumps({'command': 'extrude', 'amount': amount})
        r = requests.post(self._build_url("printer/tool"), data=data, headers=self._headers)
        return r.status_code == 204

    def select_tool(self, tool):
        data = json.dumps({'command': 'select', 'tool': tool})
        r = requests.post(self._build_url("printer/tool"), data=data, headers=self._headers)
        return r.status_code in [200, 204]

    def get_list_of_files(self):
        try:
            r = requests.get(self._build_url("files"), headers=self._headers)
        except requests.ConnectionError as e:
            logging.warning("Connection error")
            return {'files': []}
        if r.status_code in [200, 204]:
            return r.json()
        logging.warning("Unable to contact OctoPrint by REST. "
                        "Check your API key (currently '" + self._api_key + "'")
        return {'files': []}

    def download_model(self, url):
        try:
            r = requests.get(url)
        except requests.ConnectionError as e:
            return None
        if r.status_code == 200:
            logging.debug("Download OK")
            return r.content
        logging.warning("Unable to download file. Got response: " + r.status_code)
        return None

    def get_slicers(self):
        r = requests.post(self._build_url("slicing"), headers=self._headers)
        if r.status_code == 200:
            return r.json()
        logging.warning("Unable to gt slicers: " + r.status_code)
        return {}

    def _build_url(self, path):
        return f"http://{self._host}:{self._port}/api/{path}"
