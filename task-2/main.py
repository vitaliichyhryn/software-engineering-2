#  Task 2
#  * Prepare promise based alternative
#  * Write use cases for the promise based solution
#  * Write use cases for the async-await
#  * Add new on-demend feature during review
#    e.g.: Add support for parallelism
#
#  Note: for technologies that do not have the native Future-like async functionalities
#  You may combine Task 1 and 2 into a single Task that will showcase the idiomatic way of handling concurrency.

from random import random
from time import perf_counter
from multiprocessing import Pool
from typing import Any, Callable, Iterable, List 


def map_parallel(
    func: Callable,
    iter: Iterable[Any],
    *iters: Iterable[Any],
) -> List[Any]:
    results = []
    param_iters = zip(iter, *iters)
    with Pool() as pool:
        results = pool.starmap(func, param_iters)
    return results


def monte_carlo_method(n) -> float:
    points_inside = 0
    for _ in range(n):
        (x, y) = (random(), random())
        distance = x * x + y * y
        if distance <= 1:
            points_inside += 1
    return 4 * (points_inside / n)


def main() -> None:
    ns = [10 ** i for i in range(1, 9)]

    start = perf_counter()
    results = map_parallel(monte_carlo_method, ns)
    print(results)
    print(f"map_parallel: {perf_counter() - start}")

    start = perf_counter()
    results = list(map(monte_carlo_method, ns))
    print(results)
    print(f"map: {perf_counter() - start}")

if __name__ == "__main__":
    main()