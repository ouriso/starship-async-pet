class EventLoop:

  def __await__(self):
    return (yield self)


class Sleep(EventLoop):
  def __init__(self, seconds: float):
    self.seconds = seconds


async def do_sleep(times_count: int = 1):
  for _ in range(times_count):
    await Sleep(0.1)


async def sleep_ticks(times_count: int):
  ticks = do_sleep(times_count)
  await ticks
