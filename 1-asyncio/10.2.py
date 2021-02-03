import asyncio

async def generator():
    for i in range(10):
        await asyncio.sleep(1)
        yield i

async def main():
    async for item in generator():
        print(item)

asyncio.run(main())