from miniclef.pattern import Beat, Cycle, Note, Parallel, Sequence


def is_valid(pat_str: str) -> bool:
    """Check if the input string forms a valid pattern."""

    bracket_counts = {
        "[": 0,
        "(": 0,
        "<": 0,
    }
    right_brackets = {
        "]": "[",
        ")": "(",
        ">": "<",
    }

    # Check if the brackets are balanced.
    for c in pat_str:
        if c in bracket_counts:
            bracket_counts[c] += 1
        elif c in right_brackets:
            left_bracket = right_brackets[c]
            bracket_counts[left_bracket] -= 1
        if any(v < 0 for v in bracket_counts.values()):
            return False

    return all(v == 0 for v in bracket_counts.values())


def parse(pat_str: str) -> list[Beat]:
    """Parse a string pattern into a list of Beat objects."""

    # Check if the input string is valid.
    if not is_valid(pat_str):
        return []

    bracket_info = {
        "[": ("]", Sequence),
        "(": (")", Parallel),
        "<": (">", Cycle),
    }

    res = []
    while pat_str:
        if pat_str[0] in bracket_info:
            # Current character is a bracket.
            left_bracket = pat_str[0]
            right_bracket, obj = bracket_info[left_bracket]
            bracket_count = i = 0
            while i < len(pat_str):
                if pat_str[i] == left_bracket:
                    bracket_count += 1
                elif pat_str[i] == right_bracket:
                    bracket_count -= 1
                if bracket_count == 0:
                    break
                i += 1
            res.append(obj(parse(pat_str[1:i])))
            pat_str = pat_str[i + 1 :]
        elif pat_str[0] != " ":
            # Current character is not a space.
            i = 0
            while i < len(pat_str) and pat_str[i] != " ":
                i += 1
            note = pat_str[:i]
            colon_idx = note.find(":")
            if colon_idx != -1:
                res.append(Note(note[:colon_idx], note[colon_idx + 1 :]))
            else:
                res.append(Note(note, ""))
            pat_str = pat_str[i:]
        else:
            # Skip the current character.
            pat_str = pat_str[1:]

    return res
