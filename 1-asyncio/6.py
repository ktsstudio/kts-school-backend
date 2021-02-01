import socket
from selectors import DefaultSelector, EVENT_WRITE

selector = DefaultSelector()

class Future:
    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for fn in self._callbacks:
            fn(self)


class Task:
    def __init__(self, coro):
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)

    def step(self, future):
        try:
            next_future = \
                self.coro.send(future.result)
        except StopIteration:
            return

        next_future.add_done_callback(self.step)


def connect(sock, host, port):
    try:
        sock.connect((host, port))
    except BlockingIOError:
        pass

    f = Future()

    def on_connected():
        f.set_result(None)

    selector.register(sock.fileno(),
                        EVENT_WRITE,
                        on_connected)
    yield f
    selector.unregister(sock.fileno())
    print('connected')



class Fetcher:
    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblocking(False)
        # yield from connect(self.sock, 'xkcd.com', 80)
        for f in connect(self.sock, 'xkcd.com', 80):
            yield f


def loop():
    while True:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback()

# Begin fetching http://xkcd.com/353/
fetcher = Fetcher()
Task(fetcher.fetch())
loop()