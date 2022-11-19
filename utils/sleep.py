import asyncio


async def sleep(ticks=1):
    for _ in range(ticks):
        await asyncio.sleep(0)
