import heapq
import re
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
        "C": -9,
        "Cs": -8,
        "Db": -8,
        "D": -7,
        "Ds": -6,
        "Eb": -6,
        "E": -5,
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
    if note not in note_to_semitone_dist:
        return A4_FREQ

    # Calculate the semitone distance from A4.
    semitone_dist = note_to_semitone_dist[note] + (int(octave) - 4) * 12

    # Return the frequency.
    return A4_FREQ * (2 ** (semitone_dist / 12))


class NoteName:
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


class FXName:
    VIBRATO = "vibrato"


class Beat:
    def __init__(self) -> None:
        pass

    def process(self, duration: float, start_time: float, fx: list) -> None:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError


class Note(Beat):
    def __init__(self, name: str, pitch: str) -> None:
        self.name = name
        self.pitch = pitch
        self.fx = []

    def process(self, _duration: float, start_time: float, fx: list) -> None:
        self.fx = fx
        heapq.heappush(note_pq, (start_time, self))

    def play(self) -> None:
        note_name, pitch, fx = self.name, self.pitch, self.fx
        group_id = next(group)

        # Create new group.
        client.send_message("/g_new", [group_id, 0, 0])

        # Apply effects in reverse order.
        # Effects are continually added to the head of the group.
        for effect in fx[::-1]:
            fx_name, *args = effect
            match fx_name:
                case FXName.VIBRATO:
                    client.send_message("/s_new", ["vibrato", -1, 0, group_id] + args)

        # Calculate the frequency of the note.
        freq = pitch_to_freq(pitch)

        # Play the note.
        match note_name:
            case NoteName.ANGEL:
                client.send_message(
                    "/s_new", ["angel", -1, 0, group_id, "freq", freq, "amp", 1]
                )
            case NoteName.ARPY:
                client.send_message(
                    "/s_new", ["arpy", -1, 0, group_id, "freq", freq, "amp", 1]
                )
            case NoteName.BASS:
                client.send_message(
                    "/s_new", ["bass", -1, 0, group_id, "freq", freq, "amp", 1]
                )
            case NoteName.BELL:
                client.send_message(
                    "/s_new", ["bell", -1, 0, group_id, "freq", freq, "amp", 1]
                )
            case NoteName.PADS:
                client.send_message(
                    "/s_new", ["pads", -1, 0, group_id, "freq", freq, "amp", 1]
                )
            case NoteName.PLUCK:
                client.send_message(
                    "/s_new", ["pluck", -1, 0, group_id, "freq", freq, "amp", 1]
                )
            case NoteName.RIPPLE:
                client.send_message(
                    "/s_new", ["ripple", -1, 0, group_id, "freq", freq, "amp", 1]
                )
            case NoteName.SAW:
                client.send_message(
                    "/s_new", ["saw", -1, 0, group_id, "freq", freq, "amp", 1]
                )
            case NoteName.SINEPAD:
                client.send_message(
                    "/s_new", ["sinepad", -1, 0, group_id, "freq", freq, "amp", 1]
                )
            case NoteName.SITAR:
                client.send_message(
                    "/s_new", ["sitar", -1, 0, group_id, "freq", freq, "amp", 1]
                )
            case NoteName.SWELL:
                client.send_message(
                    "/s_new", ["swell", -1, 0, group_id, "freq", freq, "amp", 1]
                )

    def __lt__(self, _other) -> bool:
        return False

    def __repr__(self) -> str:
        return f"Note {self.name}{':' + self.pitch if self.pitch else ''}"


class Sequence(Beat):
    def __init__(self, beats: list[Beat]) -> None:
        self.beats = beats

    def process(self, duration: float, start_time: float, fx: list) -> None:
        new_dur = duration / len(self.beats)
        for i, beat in enumerate(self.beats):
            beat.process(new_dur, start_time + i * new_dur, fx)

    def __repr__(self) -> str:
        return f"Sequence({self.beats})"


class Parallel(Beat):
    def __init__(self, beats: list[Beat]) -> None:
        self.beats = beats

    def process(self, duration: float, start_time: float, fx: list) -> None:
        for beat in self.beats:
            beat.process(duration, start_time, fx)

    def __repr__(self) -> str:
        return f"Parallel({self.beats})"


class Cycle(Beat):
    def __init__(self, beats: list[Beat]) -> None:
        self.beats = beats
        self.i = 0

    def process(self, duration: float, start_time: float, fx: list) -> None:
        self.beats[self.i].process(duration, start_time, fx)
        self.i = (self.i + 1) % len(self.beats)

    def __repr__(self) -> str:
        return f"Cycle({self.beats})"


class Pattern:
    def __init__(self, pat_name: str, beats: list[Beat], countdown: float) -> None:
        # Initialize the pattern.
        self.pat_name = pat_name
        self.beats = beats
        self.countdown = countdown
        self.i = 0  # Index of the current beat to play.
        self.fx = []  # List of effects to apply.

        # Register the pattern.
        patterns[pat_name] = self

    # TODO: Make private/extract into outside function?
    def step(self, beat_start_time: float) -> None:
        self.beats[self.i].process(60 / get_bpm(), beat_start_time, self.fx)
        if self.i == len(self.beats) - 1:
            self.countdown -= 1
            if self.countdown == 0:
                silence(self.pat_name)
        self.i = (self.i + 1) % len(self.beats)

    def vibrato(self, rate: float = 6, depth: float = 0.02) -> Self:
        self.fx.append(("vibrato", rate, depth))
        return self

    def slide_to(self, slide: float = 1, delay: float = 0) -> Self:
        self.fx.append(("slide_to", slide, delay))
        return self

    def slide_from(self, slide: float = 1, delay: float = 0) -> Self:
        self.fx.append(("slide_from", slide, delay))
        return self

    def pitch_bend(self, bend, delay) -> Self:
        return self

    def pitch_shift(self, shift) -> Self:
        return self

    def chop(self, num_parts) -> Self:
        return self

    def coarse(self, coarse) -> Self:
        return self

    def high_pass(self, hpf, hpr) -> Self:
        return self

    def low_pass(self, lpf, lpr) -> Self:
        return self

    def bitcrush(self, bits=4, crush=8) -> Self:
        return self

    def distortion(self, dist=1) -> Self:
        return self

    def wave_shape(self, shape=1) -> Self:
        return self

    def overdrive(self, drive=1) -> Self:
        return self

    def reverb(self, room=0.5, mix=0.5) -> Self:
        return self

    def pan_spin(self, spin=0.5) -> Self:
        return self

    def formant(self, formant=0.5) -> Self:
        return self

    def tremolo(self, trem=0.5) -> Self:
        return self

    def glissando(self, gliss=0.5) -> Self:
        return self
