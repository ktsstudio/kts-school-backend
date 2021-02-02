import asyncio

import aiohttp
from aiofile import async_open


# При выполнении запроса с использование aiohttp, код выглядит более громоздким,
# относительно случая с библиотекой requests, где тот же код можно было
# уместить в одну строчку. Это сделано потому что запрос блокируется три раза:
# - при отправке запроса и получения заголовков
# - при считывания тела ответа, который может и не понадобиться
# - при освобождении ресурсов сессии
# Во время выполнения этих операций и ожидания, можно выполнять другие вещи,
# именно поэтому и нужно три await.


async def main():
    # При входе в блок с сессией создается пул соединений, которые
    # можно переиспользовать в целях оптимизации. При выходе из блока,
    # aiohttp проверяет, что все выделенные ресурсы были освобождены

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)
    ) as session:
        # HTTP-запрос является ассинхронной операцией ввода/вывода,
        # поэтому добавляется в цикл исполнения, до тех пор, пока не придет ответ
        async with session.get("https://foodish-api.herokuapp.com/api") as response:
            # Запрос прерывается, считывая только заголовки, поэтому можно синхронно
            # получить status ответа, но для получения тела ответа
            # придется вызывать соответствующий метод ассинхронно
            print(f"HTTP Response Status: {response.status}")
            json_data = await response.json()
            image_url = json_data["image"]
            extension = image_url.split(".")[-1]
            print(f"Image URL: {image_url}")

        async with session.get(image_url) as response:
            total_bytes, wrote_bytes = response.headers["Content-Length"], 0
            print("Open file...")
            async with async_open(f"random_food_image.{extension}", "wb") as f:
                print("Writing image bytes...")
                # Считываем кусочки данных в том порядке и размере,
                # в которых мы получаем их с сервера.
                # В моменты между получение и записью новых кусочков данных,
                # интерпретатор может выполнять какие-то другие операции
                async for data, _ in response.content.iter_chunks():
                    wrote_bytes += len(data)
                    await f.write(data)
                    print(f"Wrote {wrote_bytes}/{total_bytes}")
        global started
        started = False


# Простой счетчик, который позволяет увидеть, что операции в клиенте ассинхронны
# и в моменты ожидания, возможно выполнение другого кода.
async def simple_counter():
    global started
    while started:
        await asyncio.sleep(0.1)
        print("another operation")


started = True


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
# loop.run_until_complete(asyncio.gather(main(), simple_counter()))
