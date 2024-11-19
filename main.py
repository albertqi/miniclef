import heapq
import threading
import time
from miniclef.clock import get_bpm
from miniclef.vars import note_pq, patterns


def main() -> None:
    beat_start_time = time.time()
    while True:
        # Get the current time.
        now = time.time()

        # Play any notes that are due.
        while note_pq and note_pq[0][0] <= now:
            _, note = heapq.heappop(note_pq)
            note.play()

        # Wait for the next beat.
        if now < beat_start_time + (60 / get_bpm()):
            continue
        beat_start_time = now

        # Play the next beat in each pattern.
        # We use 'list' to allow 'patterns' to be modified during iteration.
        for pattern in list(patterns.values()):
            pattern.step(beat_start_time)

        # TODO: Generate sheet music.


threading.Thread(target=main, daemon=True).start()
