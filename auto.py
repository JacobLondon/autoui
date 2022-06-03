import threading
import pyautogui as pag
import time

class Event:
    def __init__(self, name: str, message: str):
        self.name = name
        self.message = message

class EventQueue:
    def __init__(self):
        self.events = []
        self.lock = threading.Semaphore()

    def enqueue(self, event: Event):
        if event is None: return
        self.lock.acquire()
        # unique only
        if not any(qitem.name == event.name for qitem in self.events):
            self.events.append(event)
        self.lock.release()

    def dequeue(self) -> Event:
        event: Event = None
        self.lock.acquire()
        if self.events:
            event = self.events.pop()
        self.lock.release()
        return event

class EventConsumer:
    def __init__(self, looking_for):
        self.name = looking_for
    def consume(self, some_event: Event):
        if some_event.name == self.name:
            self.action(some_event.message)
    def action(self, message) -> None:
        raise NotImplementedError('child needs to implement')

class EventProducer:
    def __init__(self):
        self.event = None
    def produce(self) -> Event:
        self.event = self.action()
        return self.event
    def action(self) -> Event:
        raise NotImplementedError('child needs to implement')

class Mediator:
    def __init__(self, producers, consumers, period=0.1):
        self.events = EventQueue()
        self.thread: threading.Thread = threading.Thread(target=self.run)
        self._done = False
        self._period = period

        self.producers = producers
        self.consumers = consumers

    def start(self):
        self.thread.start()

    def stop(self):
        self._done = True
        self.thread.join()

    # manually produce instead of using a standalone producer
    def send(self, event: Event):
        self.events.enqueue(event)

    def execute_event(self, event: Event):
        for consumer in self.consumers:
            if consumer.name == event.name:
                consumer.action(event.message)

    def run(self):
        while not self._done:
            for producer in self.producers:
                event = producer.produce()
                self.events.enqueue(event)

            while True:
                event = self.events.dequeue()
                if event is None: break
                self.execute_event(event)

            time.sleep(self._period)

################################################################################
# Implementation
################################################################################

class MyMouseProducer(EventProducer):
    def action(self) -> Event:
        x, y = pag.position()
        message = "%d, %d" % (x, y)
        return Event("mouse", message)

class MyPrintConsumer(EventConsumer):
    def action(self, message) -> None:
        print(message)

def _main(argv):
    m = Mediator(
        producers=[
            MyMouseProducer()
        ],
        consumers=[
            MyPrintConsumer("mouse")
        ])
    m.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    m.stop()

    return 0

if __name__ == '__main__':
    import sys
    exit(_main(sys.argv))
