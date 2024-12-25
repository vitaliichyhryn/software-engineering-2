# Task 4 (Stream/AsyncIterator/Alternative) -- Ongoing processing of large data sets that do not fit in memory

import asyncio
import hashlib
from random import randint
from typing import AsyncGenerator, List


async def stream_str(
        source: List[str]
) -> AsyncGenerator[str]:
    for chunk in source:
        delay = randint(0, 3)
        await asyncio.sleep(delay)
        yield chunk


async def get_str_sha256(
    stream: AsyncGenerator
) -> str:
    hasher = hashlib.sha256()
    async for chunk in stream:
        print(f"Got chunk: {chunk}")
        hasher.update(chunk.encode("utf-8"))
    return hasher.hexdigest()


async def main() -> None:
    important_data = [
        "Important ",
        "data.",
    ]
    complex_password = [
        "Complex ",
        "password."
    ]
    task = asyncio.gather(
        get_str_sha256(stream_str(important_data)),
        get_str_sha256(stream_str(complex_password))
    )
    result = await task
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
