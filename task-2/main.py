# Task 2
# * Prepare promise based alternative
# * Write use cases for the promise based solution
# * Write use cases for the async-await
# * Add new on-demend feature during review
#   e.g.: Add support for parallelism
#
# Note: for technologies that do not have the native Future-like async functionalities
# You may combine Task 1 and 2 into a single Task that will showcase the idiomatic way of handling concurrency.

import asyncio, functools
from typing import Any, Callable, Iterable, List 
from random import randint

responses = {
    "foo.com": {"message": "Hello from foo.com!"},
    "bar.com": {"message": "Hello from bar.com!"},
    "baz.com": {"message": "Hello from baz.com!"},
}


def debounce(
    timeframe: float,
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        lock = asyncio.Lock()
        called: float | None = None

        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            nonlocal called, lock
            loop = asyncio.get_event_loop()
            async with lock:
                if called:
                    now = loop.time()
                    elapsed = now - called

                    if elapsed < timeframe:
                        left = timeframe - elapsed
                        await asyncio.sleep(left)
                        print(f"Slept for {left} seconds.")

            called = loop.time()
            return await func(*args, **kwargs)
        return wrapped
    return wrapper


async def map_async(
    function: Callable,
    iterable: Iterable[Any],
) -> List[Any]:
    awaits = [function(item) for item in iterable]
    tasks = asyncio.gather(*awaits)
    result = await tasks
    return result


@debounce(timeframe=3)
async def send_request(
        endpoint
) -> dict[str, str] | None:
    delay = randint(0, 5)
    await asyncio.sleep(delay)
    print(f"Request to {endpoint} took {delay} seconds to complete.")
    response: dict[str, str] | None = responses.get(endpoint)
    if response:
        message: str | None = response.get("message")
        if message:
            print(f"Got message: {message}")
    return response


async def main() -> None:
    endpoints = responses.keys()
    task = asyncio.create_task(
        map_async(send_request, endpoints)
    )
    result = await task
    print(result)

if __name__ == "__main__":
    asyncio.run(main()) 
