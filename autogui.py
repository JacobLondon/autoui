#!/usr/bin/env python3
import time
import threading
import pyautogui as pag
import os

from events import (
    Event,
    EventConsumer,
    EventProducer,
    EventMediator,
)
from menu import MenuMediator
from transformer import xmouse, xform

CHECKPOINT = 'autogui.checkpoint'

def try_write(filename: str, data: str):
    if not filename:
        print("Cannot write: no file specified")
        return

    try:
        with open(filename, "w") as fp:
            fp.write(data)
    except OSError:
        print(f"Cannot write: {filename}")

def try_read(filename: str) -> str:
    if not filename:
        print("Cannot open: no file specified")
        return None

    try:
        with open(filename, "r") as fp:
            return fp.read()
    except OSError:
        print(f"Cannot open: {filename} not allowed")
    return None

def command_is_probably_safe(shell_command: str) -> bool:
    # not safe if any scary chars are in shell command
    scary_chars = (';', '&', '|', '&&', '||', '>', '>>', '<', '<<')
    if any(char in shell_command for char in scary_chars):
        return False
    return True


class MyMouseProducer(EventProducer):
    def action(self, data: 'MyState') -> Event:
        x, y = pag.position()
        message: str = f"{x}, {y}"
        return Event("mouse", message)

class MyMouseConsumer(EventConsumer):
    def action(self, message: str, data: 'MyState'):
        data.mediator.set_coords(message)

class MyCoordsConsumer(EventConsumer):
    def action(self, mediator: MenuMediator, data: 'MyState'):
        mouse_cmd = xmouse(mediator.get_coords())
        mediator.append_text(mouse_cmd)

class MySaveConsumer(EventConsumer):
    def action(self, mediator: MenuMediator, data: 'MyState'):
        # try to parse first to check for errors
        text = mediator.get_text()
        transformed = xform(text)
        if transformed is None: return

        # then check if the file exists to write to
        filename = mediator.get_url()
        if not filename:
            print("Cannot save: no file specified")
            return
        if not command_is_probably_safe(filename):
            print("Cannot save: Invalid characters in filename")
            return

        filenamepy = f"{filename}.py"
        try_write(filenamepy, transformed)
        try_write(filename, text)

        try_write(CHECKPOINT, filename)

class MyOpenConsumer(EventConsumer):
    def action(self, mediator: MenuMediator, data: 'MyState'):
        filename = mediator.get_url()
        text = try_read(filename)
        if text is None: return

        mediator.delete_text()
        mediator.append_text(text)

class MyPlayConsumer(EventConsumer):
    def action(self, mediator: MenuMediator, data: 'MyState'):
        filename = mediator.get_url()
        if not filename:
            print("Cannot play: No file specified")
            return

        if not command_is_probably_safe(filename):
            print("Cannot play: Unsafe text in the URL!")
            return

        command = f"python {filename}.py"
        print(f"Running {filename}...")
        os.system(command)

class MyStartupConsumer(EventConsumer):
    def action(self, mediator: MenuMediator, data: 'MyState'):
        checkpoint = try_read(CHECKPOINT)
        if checkpoint is None: return

        # fine... we store it here
        mediator.set_url(checkpoint)


class MyState:
    def __init__(self):
        producers = [
            MyMouseProducer(self),
        ]
        consumers = [
            MyMouseConsumer("mouse", self),
            MyCoordsConsumer("coords", self),
            MySaveConsumer("save", self),
            MyOpenConsumer("open", self),
            MyPlayConsumer("play", self),
            MyStartupConsumer("startup", self),
        ]
        self.eventer = EventMediator(producers, consumers)
        self.mediator = MenuMediator("AutoGUI",
            self.save_to_file_func,
            self.open_file_func,
            self.coord_save_func,
            self.play_func)

        def startup_thread():
            time.sleep(0.25)
            self.eventer.produce("startup", self.mediator)
            self.eventer.produce("open", self.mediator)
        self.startup_thread = threading.Thread(target=startup_thread)

    def start(self):
        self.eventer.start()
        self.startup_thread.start()
        self.mediator.start()
        self.eventer.stop()
        self.startup_thread.join()

    # press hotkey to insert coords into textbox
    def coord_save_func(self, mediator):
        self.eventer.produce("coords", mediator)

    def save_to_file_func(self, mediator):
        self.eventer.produce("save", mediator)

    def open_file_func(self, mediator):
        self.eventer.produce("open", mediator)

    def play_func(self, mediator):
        self.eventer.produce("save", mediator)
        self.eventer.produce("play", mediator)

def _main(argv):
    m = MyState()
    m.start()
    return 0

if __name__ == '__main__':
    import sys
    exit(_main(sys.argv))
