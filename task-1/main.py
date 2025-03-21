# Task 1
# * Choose array fn (map/filter/filterMap/some/find/findIndex)
# * Prepare its callback based async counterpart
# * Prepare demo cases for the usage
# * Add new on-demend feature during review
#   e.g.: Add support for debounce (if the task took less then X time to
#   complete -- add an additional execution delay)

import asyncio
from asyncio.tasks import Task
from typing import Any, Callable, Iterable, List
from random import randint

responses = {
    "foo.com": {"message": "Hello from foo.com!"},
    "bar.com": {"message": "Hello from bar.com!"},
    "baz.com": {"message": "Hello from baz.com!"},
}


async def map_callback(
    function: Callable,
    callback: Callable,
    iterable: Iterable,
) -> List[Any]:
    async with asyncio.TaskGroup() as task_group:
        tasks: List[Task] = []
        for item in iterable:
            task = task_group.create_task(function(item))
            task.add_done_callback(callback)
            tasks.append(task)
    result = [task.result() for task in tasks]
    return result


async def send_request(
    endpoint: str
) -> dict[str, str] | None:
    delay = randint(0, 5)
    await asyncio.sleep(delay)
    print(f"Request to {endpoint} took {delay} seconds to complete.")
    response: dict[str, str] | None = responses.get(endpoint)
    return response


def on_response_got(
    future: asyncio.Future
) -> None:
    response: dict[str, str] | None = future.result()
    if not response:
        return
    message = response.get("message")
    if not message:
        return
    print(f"Got message: {message}")


async def main() -> None:
    endpoints = responses.keys()
    task = asyncio.create_task(
        map_callback(send_request, on_response_got, endpoints)
    )
    result = await task
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
