import time
import subprocess
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.process = subprocess.Popen([sys.executable, script])

    def on_modified(self, event):
        if event.src_path.endswith('.py'):  # Restart only if Python files are modified
            self.process.terminate()
            self.process = subprocess.Popen([sys.executable, self.script])

if __name__ == "__main__":
    script_to_watch = "dashboard.py"  # Replace with your main script
    event_handler = ReloadHandler(script_to_watch)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()