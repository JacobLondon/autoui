import pyautogui as pag

from events import (
    Event,
    EventConsumer,
    EventProducer,
    EventMediator,
)
from menu import MenuMediator

class MyMouseProducer(EventProducer):
    def action(self, data: 'MyState') -> Event:
        x, y = pag.position()
        message = "%d, %d" % (x, y)
        return Event("mouse", message)

class MyMouseConsumer(EventConsumer):
    def action(self, message, data: 'MyState'):
        data.mediator.set_coords(message)

class MyCoordsConsumer(EventConsumer):
    def action(self, message: MenuMediator, data: 'MyState'):
        data.mediator.append_text(message.get_coords())

class MySaveConsumer(EventConsumer):
    def action(self, message: MenuMediator, data: 'MyState'):
        filename = message.get_url()
        text = message.get_text()

        try:
            with open(filename, "w") as fp:
                fp.write(text)
        except OSError:
            print("Failed to write %s" % filename)

class MyOpenConsumer(EventConsumer):
    def action(self, message: MenuMediator, data: 'MyState'):
        filename = message.get_url()
        try:
            with open(filename, "r") as fp:
                text = fp.read()
        except OSError:
            print("Failed to open %s" % filename)
            return

        message.delete_text()
        message.append_text(text)


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
        ]
        self.eventer = EventMediator(producers, consumers)
        self.mediator = MenuMediator("AutoGUI",
            self.save_to_file_func, self.open_file_func, self.coord_save_func)

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

def _main(argv):
    m = MyState()
    m.start()
    return 0

if __name__ == '__main__':
    import sys
    exit(_main(sys.argv))
