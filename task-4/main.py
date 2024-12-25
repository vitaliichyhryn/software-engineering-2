# Task 4 (Stream/AsyncIterator/Alternative) -- Ongoing processing of large data sets that do not fit in memory

import asyncio
import hashlib
from random import randint


async def stream(source):
    for chunk in source:
        delay = randint(0, 3)
        await asyncio.sleep(delay)
        yield chunk


async def get_sha256(
    stream
):
    hasher = hashlib.sha256()
    async for chunk in stream:
        print(f"Got chunk: {chunk}")
        hasher.update(chunk.encode("utf-8"))
    return hasher.hexdigest()


async def main():
    chunked_string = [
        "Some ",
        "important ",
        "data.",
    ]
    other_chunked_string = [
        "Hash ",
        "this.",
    ]
    task = asyncio.gather(
        get_sha256(stream(chunked_string)),
        get_sha256(stream(other_chunked_string))
    )
    result = await task
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
