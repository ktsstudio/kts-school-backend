import asyncio

class AsyncIterator:
    def __init__(self, arr: list[int]):
        self._arr = arr
        self._pos = -1

    def __aiter__(self):
        return self
    
    async def __anext__(self):
        await asyncio.sleep(1)
        self._pos += 1

        if len(self._arr) == 0 or self._pos >= len(self._arr):
            raise StopAsyncIteration
            
        return self._arr[self._pos]

async def main():
    iterator = AsyncIterator([1, 2, 3, 4, 5])
    async for item in iterator:
        print(item)

asyncio.run(main())