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


def try_write(filename: str, data: str):
    try:
        with open(filename, "w") as fp:
            fp.write(data)
    except OSError:
        print("Failed to write", filename)

def try_read(filename: str) -> str:
    try:
        with open(filename, "r") as fp:
            return fp.read()
    except OSError:
        print("Failed to open", filename)
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
        message: str = "%d, %d" % (x, y)
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

        filenamepy = filename + ".py"
        try_write(filenamepy, transformed)
        try_write(filename, text)

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
            print("Cannot play: no file specified")
            return

        if not command_is_probably_safe(filename):
            print("Unsafe text in the URL!")
            return

        command = f"python {filename}.py"
        os.system(command)

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
        ]
        self.eventer = EventMediator(producers, consumers)
        self.mediator = MenuMediator("AutoGUI",
            self.save_to_file_func,
            self.open_file_func,
            self.coord_save_func,
            self.play_func)

    def start(self):
        self.eventer.start()
        self.mediator.start()
        self.eventer.stop()

    # press hotkey to insert coords into textbox
    def coord_save_func(self, mediator):
        self.eventer.send("coords", mediator)

    def save_to_file_func(self, mediator):
        self.eventer.send("save", mediator)

    def open_file_func(self, mediator):
        self.eventer.send("open", mediator)

    def play_func(self, mediator):
        self.eventer.send("save", mediator)
        self.eventer.send("play", mediator)

def _main(argv):
    m = MyState()
    m.start()
    return 0

if __name__ == '__main__':
    import sys
    exit(_main(sys.argv))
