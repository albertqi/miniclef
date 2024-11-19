from miniclef.parse import parse
from miniclef.pattern import Pattern


def repeat(count: float, pat_name: str, pat_str: str) -> Pattern:
    """Play a pattern a certain number of times."""
    return Pattern(pat_name, parse(pat_str), count)


def loop(pat_name: str, pat_str: str) -> Pattern:
    """Play a pattern indefinitely."""
    return repeat(float("inf"), pat_name, pat_str)


def once(pat_name: str, pat_str: str) -> Pattern:
    """Play a pattern one time."""
    return repeat(1, pat_name, pat_str)


def twice(pat_name: str, pat_str: str) -> Pattern:
    """Play a pattern two times."""
    return repeat(2, pat_name, pat_str)


def thrice(pat_name: str, pat_str: str) -> Pattern:
    """Play a pattern three times."""
    return repeat(3, pat_name, pat_str)
