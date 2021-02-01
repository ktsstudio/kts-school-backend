import asyncio

async def square(val):
  await asyncio.sleep(2)
  return val * val
 

async def main():
  sq5, sq6, sq7 = await asyncio.gather(
      square(5),
      square(6),
      square(7)
  )
  print(sq5, sq6, sq7)


asyncio.run(main())