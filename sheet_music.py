import abjad
from miniclef.clock import get_bpm
from miniclef.vars import patterns


def gen_sheet_music() -> None:
    """Generate sheet music for all patterns."""

    if not list(patterns.values()):
        return

    def find_first_attachable(obj: abjad.Component) -> abjad.Component:
        """Find the first attachable object in a container."""
        if isinstance(obj, abjad.Container):
            return find_first_attachable(obj[0])
        return obj

    staffs = []
    for pattern in list(patterns.values()):
        staffs.append(abjad.Staff(pattern.gen_lilypond_staff()))
        try:
            obj = find_first_attachable(staffs[-1])
            abjad.attach(abjad.InstrumentName(f'"{pattern.pat_name}"'), obj)
        except Exception as e:
            print(e)
    try:
        obj = find_first_attachable(staffs[0])
        abjad.attach(abjad.MetronomeMark(abjad.Duration(1, 4), get_bpm()), obj)
    except Exception as e:
        print(e)
    score = abjad.Score(staffs)
    abjad.persist.as_pdf(score, "sheet_music.pdf")
