import heapq
import random
import re
from enum import Enum
from miniclef.clock import get_bpm
from miniclef.server import client
from miniclef.vars import group, note_pq, patterns, silence
from typing import Self


def pitch_to_freq(pitch: str) -> float:
    """Convert a pitch string to a frequency."""

    # Define the reference frequency for A4.
    A4_FREQ = 440.0

    # Define the semitone distance from A for each note.
    note_to_semitone_dist = {
        "Cb": -10,
        "C": -9,
        "Cs": -8,
        "Db": -8,
        "D": -7,
        "Ds": -6,
        "Eb": -6,
        "E": -5,
        "Es": -4,
        "Fb": -5,
        "F": -4,
        "Fs": -3,
        "Gb": -3,
        "G": -2,
        "Gs": -1,
        "Ab": -1,
        "A": 0,
        "As": 1,
        "Bb": 1,
        "B": 2,
        "Bs": 3,
    }

    # Parse the pitch string.
    match = re.fullmatch(r"([A-Ga-g])([bfs#]?)(\d?)", pitch)
    if not match:
        return A4_FREQ

    # Extract components from the matched groups.
    note = match.group(1).upper()  # Note letter (i.e., C, D, E, F, G, A, B).
    accidental = match.group(2)  # Accidental (i.e., b, f, s, #).
    octave = match.group(3) or "4"  # Octave number.

    # Adjust note for sharps and flats.
    if accidental in ("b", "f"):
        note += "b"
    elif accidental in ("s", "#"):
        note += "s"

    # Check if the note is valid.
    assert note in note_to_semitone_dist

    # Calculate the semitone distance from A4.
    semitone_dist = note_to_semitone_dist[note] + (int(octave) - 4) * 12

    # Return the frequency.
    return A4_FREQ * (2 ** (semitone_dist / 12))


def pitch_to_lilypond(pitch: str) -> str:
    """Convert a pitch string to a LilyPond note."""

    # Parse the pitch string.
    match = re.fullmatch(r"([A-Ga-g])([bfs#]?)(\d?)", pitch)
    if not match:
        return "a'"

    # Extract components from the matched groups.
    note = match.group(1).lower()  # Note letter (i.e., c, d, e, f, g, a, b).
    accidental = match.group(2)  # Accidental (i.e., b, f, s, #).
    octave = match.group(3) or "4"  # Octave number.

    # Adjust note for sharps and flats.
    if accidental in ("b", "f"):
        note += "f"
    elif accidental in ("s", "#"):
        note += "s"

    # Calculate the distance from the third octave.
    dist_from_3 = int(octave) - 3
    if dist_from_3 > 0:
        return note + "'" * dist_from_3
    elif dist_from_3 < 0:
        return note + "," * -dist_from_3

    # Return the LilyPond note.
    return note


class NoteName(Enum):
    ANGEL = "angel"
    ARPY = "arpy"
    BASS = "bass"
    BELL = "bell"
    PADS = "pads"
    PLUCK = "pluck"
    RIPPLE = "ripple"
    SAW = "saw"
    SINEPAD = "sinepad"
    SITAR = "sitar"
    SWELL = "swell"


class Beat:
    def __init__(self) -> None:
        pass

    def process(self, duration: float, start_time: float) -> None:
        raise NotImplementedError

    def gen_lilypond(self, note_val: int) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError


class Note(Beat):
    def __init__(self, name: str, pitch: str) -> None:
        self.name = name
        self.pitch = pitch

    def process(self, _duration: float, start_time: float) -> None:
        heapq.heappush(note_pq, (start_time, self))

    def gen_lilypond(self, note_val: int) -> str:
        if self.name not in set([item.value for item in NoteName]):
            return f"r{note_val}"
        return f"{pitch_to_lilypond(self.pitch)}{note_val}"

    def play(self) -> None:
        note_name, pitch = self.name, self.pitch

        # Ensure that the note name is valid.
        if note_name not in set([item.value for item in NoteName]):
            return

        # Create new group.
        group_id = next(group)
        client.send_message("/g_new", [group_id, 0, 0])

        # Calculate the frequency of the note.
        freq = pitch_to_freq(pitch)

        # Play the note.
        client.send_message(
            "/s_new", [note_name, -1, 0, group_id, "freq", freq, "amp", 1]
        )

    def __lt__(self, _other: Self) -> bool:
        return False

    def __repr__(self) -> str:
        return f"Note {self.name}{':' + self.pitch if self.pitch else ''}"


class Sequence(Beat):
    def __init__(self, beats: list[Beat]) -> None:
        self.beats = beats

    def process(self, duration: float, start_time: float) -> None:
        new_dur = duration / len(self.beats)
        for i, beat in enumerate(self.beats):
            beat.process(new_dur, start_time + i * new_dur)

    def gen_lilypond(self, note_val: int) -> str:
        def highest_power_of_2(n: int) -> int:
            """Return the highest power of 2 that is less than or equal to n."""
            p = 1
            while p <= n:
                p *= 2
            return p // 2

        hp_2 = highest_power_of_2(len(self.beats))
        return (
            "\\tuplet "
            + f"{len(self.beats)}/{hp_2}"
            + " { "
            + " ".join([beat.gen_lilypond(note_val * hp_2) for beat in self.beats])
            + " }"
        )

    def __repr__(self) -> str:
        return f"Sequence({self.beats})"


class Parallel(Beat):
    def __init__(self, beats: list[Beat]) -> None:
        self.beats = beats

    def process(self, duration: float, start_time: float) -> None:
        for beat in self.beats:
            beat.process(duration, start_time)

    def gen_lilypond(self, note_val: int) -> str:
        return (
            "\\new Voice << "
            + " ".join(
                ["{ " + beat.gen_lilypond(note_val) + " }" for beat in self.beats]
            )
            + " >>"
        )

    def __repr__(self) -> str:
        return f"Parallel({self.beats})"


class Cycle(Beat):
    def __init__(self, beats: list[Beat]) -> None:
        self.beats = beats
        self.i = 0

    def process(self, duration: float, start_time: float) -> None:
        self.beats[self.i].process(duration, start_time)
        self.i = (self.i + 1) % len(self.beats)

    def gen_lilypond(self, note_val: int) -> str:
        return self.beats[self.i].gen_lilypond(note_val)

    def __repr__(self) -> str:
        return f"Cycle({self.beats})"


class Random(Beat):
    def __init__(self, beats: list[Beat]) -> None:
        self.beats = beats
        self.beat_to_play = random.choice(self.beats)

    def process(self, duration: float, start_time: float) -> None:
        self.beat_to_play.process(duration, start_time)
        self.beat_to_play = random.choice(self.beats)

    def gen_lilypond(self, note_val: int) -> str:
        return self.beat_to_play.gen_lilypond(note_val)

    def __repr__(self) -> str:
        return f"Random({self.beats})"


class Pattern:
    def __init__(self, pat_name: str, beats: list[Beat], countdown: float) -> None:
        # Initialize the pattern.
        self.pat_name = pat_name
        self.beats = beats
        self.countdown = countdown
        self.i = 0  # Index of the current beat to play.

        # Register the pattern.
        patterns[pat_name] = self

    def step(self, beat_start_time: float) -> None:
        self.beats[self.i].process(60 / get_bpm(), beat_start_time)
        if self.i == len(self.beats) - 1:
            self.countdown -= 1
            if self.countdown == 0:
                silence(self.pat_name)
        self.i = (self.i + 1) % len(self.beats)

    def gen_lilypond_staff(self) -> str:
        return " ".join(beat.gen_lilypond(4) for beat in self.beats)
