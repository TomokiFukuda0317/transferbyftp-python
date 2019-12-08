from __future__ import print_function

import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class MyHandler(PatternMatchingEventHandler):
    def __init__(self, command, patterns):
        super(MyHandler, self).__init__(patterns=patterns)
        self.command = command

    def _run_command(self):
        subprocess.call([self.command, ])

    def on_moved(self, event):
        print("called on_moved")

    def on_created(self, event):
        print("called on_created")

    def on_deleted(self, event):
        print("called on_deleted")

    def on_modified(self, event):
        print("called on_modified")

def watch(path, command, extensions):
    event_handler = MyHandler(command, extensions)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    watch("./", "ls", ["*.log"])