class EventLoop:
    def __await__(self):
        return (yield self)


class Sleep(EventLoop):
    def __init__(self, seconds: float):
        self.seconds = seconds
