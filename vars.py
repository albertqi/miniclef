import heapq
from typing import Generator


def gen_group_id() -> Generator[int, None, None]:
    """Generate unique group IDs."""
    i = 1
    while True:
        yield i
        i += 1


group = gen_group_id()
patterns = {}  # {pat_name: Pattern}
note_pq = []  # [(start_time, Note)]
heapq.heapify(note_pq)


def hush() -> None:
    """Stop all patterns."""
    patterns.clear()


def silence(pat_name: str) -> None:
    """Stop a pattern."""
    patterns.pop(pat_name, None)
