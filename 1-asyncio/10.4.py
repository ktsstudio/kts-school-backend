import asyncio

class AsyncManager:
    def __init__(self):
        pass

    async def __aenter__(self):
        await asyncio.sleep(1)
        print('finished __aenter__')
        return self

    async def __aexit__(self, *args):
        await asyncio.sleep(1)
        print('finished __aexit__')


async def main():
    async with AsyncManager():
        print('inside manager')

asyncio.run(main())