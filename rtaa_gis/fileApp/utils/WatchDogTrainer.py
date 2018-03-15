import subprocess
import os
import sys
import traceback
from rtaa_gis.settings import BASE_DIR


def open_monitor(in_path):
    try:
        a = subprocess.Popen(['python', os.path.join(os.path.dirname(os.path.abspath(__file__)), "watch_dog.py"), in_path])
        return {a.pid: {"process_path": in_path, "process": a}}
    except:
        lumber_stack()


def lumber_stack():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exc(file=sys.stdout)
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=sys.stdout)


class Observers:
    def __init__(self, paths):
        self.paths = paths
        self.processes = {}
        return

    def stop_monitors(self):
        for k, v in iter(self.processes.items()):
            try:
                v["process"].kill()
                v["process"] = ""
            except:
                lumber_stack()

        for k in list(self.processes.keys()):
            if self.processes[k]["process"] == "":
                del self.processes[k]
        paths = [{"pid": k, "path": v["process_path"]} for k, v in self.processes.items()]
        return paths

    def start_monitors(self):
        for path in self.paths:
            try:
                monitor_exists = False
                for k, v in self.processes.items():
                    if path == v["process_path"]:
                        monitor_exists = True
                if not monitor_exists:
                    x = open_monitor(path)
                    pid = list(x.keys())[0]
                    self.processes[pid] = x[pid]

            except:
                lumber_stack()

        paths = [{"pid": k, "path": v["process_path"]} for k, v in self.processes.items()]
        return paths


if __name__ == "__main__":
    obs = Observers([r"C:\\"])
    try:
        obs.start_monitors()
    except:
        obs.stop_monitors()