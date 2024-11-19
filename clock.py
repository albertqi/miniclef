bpm = 135


def set_bpm(new_bpm: float) -> None:
    """Set the global BPM."""
    global bpm
    bpm = new_bpm


def get_bpm() -> float:
    """Get the global BPM."""
    return bpm
