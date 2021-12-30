from typing import Generator, Iterable, List, TypeVar

T = TypeVar("T")


def batch(iterable: Iterable[T], batch_size: int, drop_reminder: bool = False) -> Generator[List[T], None, None]:
    item_batch = []

    for item in iterable:
        item_batch.append(item)

        if len(item_batch) == batch_size:
            yield item_batch
            item_batch = []

    if item_batch and not drop_reminder:
        yield item_batch
