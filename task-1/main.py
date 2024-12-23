# Task 1
# * Choose array fn (map/filter/filterMap/some/find/findIndex)
# * Prepare its callback based async counterpart
# * Prepare demo cases for the usage
# * Add new on-demend feature during review
#   e.g.: Add support for debounce (if the task took less then X time to
#   complete -- add an additional execution delay)

import asyncio, functools
from typing import Any, Awaitable, Callable, Iterable, List 

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
                        print("debounced")
                        await asyncio.sleep(timeframe - elapsed)
                        print("slept")

            called = loop.time()
            return await func(*args, **kwargs)
        return wrapped
    return wrapper

@debounce(timeframe=3)
async def map_async(
    func: Callable[..., Awaitable],
    iter: Iterable[Any],
    *iters: Iterable[Any],
) -> List[Any]:
    param_iters = zip(iter, *iters)
    awaits = [func(*param_iter) for param_iter in param_iters]
    return await asyncio.gather(*awaits)


async def lower_async(string: str) -> str:
    await asyncio.sleep(1)
    return string.lower()


async def pow_async(base: int, power: int) -> int:
    await asyncio.sleep(3)
    return base ** power


async def main() -> None:
    tasks = [
        map_async(lower_async, ["ABC", "DEF"]),
        *[map_async(pow_async, [2, 4], [1, 2]) for _ in range(3)],
        map_async(lower_async, ["HIJ", "KLM"]),
    ]
    results = await asyncio.gather(*tasks)
    [print(result) for result in results]

if __name__ == "__main__":
    asyncio.run(main()) 
