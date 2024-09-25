"""File system observer.

Monitors source files and executes a callback function when any of them changes.
To be used with the --watch option.
"""

import logging
import time
from os import path
from typing import Callable, TypeAlias

from watchdog.events import DirModifiedEvent, FileModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer

POLL_TIME = 1
DEBOUNCE_TIME = 3

logger = logging.getLogger("Watch")
_most_recent_calls: dict[str, float] = {}

CallbackFunction: TypeAlias = Callable[[], None]


class _EventHandler(FileSystemEventHandler):
    callback: CallbackFunction
    extension: str

    def __init__(self, extension: str, callback: CallbackFunction):
        super().__init__()
        self.callback = callback
        self.extension = extension

    def on_modified(self, event: FileModifiedEvent | DirModifiedEvent) -> None:
        if event.event_type == "modified" and not event.is_directory:
            _, ext = path.splitext(str(event.src_path))
            if ext == self.extension and not _debounced(str(event.src_path)):
                self.callback()


def _debounced(name: str) -> bool:
    now = time.time()
    if name in _most_recent_calls and now - _most_recent_calls[name] < DEBOUNCE_TIME:
        return True
    _most_recent_calls[name] = now
    return False


def run_file_observer(dir: str, extension: str, callback: CallbackFunction) -> None:
    observer = Observer()
    observer.schedule(_EventHandler(extension, callback), dir, recursive=True)
    observer.start()
    logger.info("Waiting for changes in %s, CTRL+C to exit", dir)
    try:
        while observer.is_alive():
            observer.join(POLL_TIME)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()
