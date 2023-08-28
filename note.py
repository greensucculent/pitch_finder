import re
from frequency import *

# Map of flat notes to their sharp equivalent.
FLAT_TO_SHARP = {
    D_NOTE + FLAT_SYMBOL: CSHARP_NOTE,
    E_NOTE + FLAT_SYMBOL: DSHARP_NOTE,
    G_NOTE + FLAT_SYMBOL: FSHARP_NOTE,
    A_NOTE + FLAT_SYMBOL: GSHARP_NOTE,
    B_NOTE + FLAT_SYMBOL: ASHARP_NOTE,
}

# Regular expressions for validating notes
_BASE_REGEX = f"[A-G]({SHARP_SYMBOL}|#|{FLAT_SYMBOL}|b|{NATURAL_SYMBOL})?"
NOTE_REGEX = f"^{_BASE_REGEX}$"
NOTEOCTAVE_REGEX = f"^{_BASE_REGEX}(0|10?|[2-9])$"


class Note():
    """
    Note represents a note on the standard 12-note scale within any octave from 0 to 12.
    Fields:
        - note: name of note without octave
        - octave: octave of note
        - freq: frequency of note
    The string representation of Note puts the "note" and "octave" fields
    together, e.g. B♯ in the 6th octave becomes 'B♯6'.
    """

    def __init__(self, note, octave):
        # Validate the note.
        result = re.fullmatch(NOTE_REGEX, note)
        if result is None:
            raise ValueError(f'Invalid note: "{note}"')

        # Handle musical symbols that are not the standard sharp symbol.
        if len(note) > 1 and note[1] != SHARP_SYMBOL:
            # Standardize sharp symbols.
            if note[1] == '#':
                note = note[0] + SHARP_SYMBOL

            # Standardize flat symbols, and convert the note into a sharp to match our tables.
            if note[1] == 'b':
                note = note[0] + FLAT_SYMBOL
            if note[1] == FLAT_SYMBOL:
                note = FLAT_TO_SHARP[note]

            # Drop natural symbols.
            if note[1] == NATURAL_SYMBOL:
                note = note[:1]

        if note not in FREQ_TABLE:
            raise ValueError(f'Invalid note: "{note}"')

        # Make sure we have a valid integer for the octave.
        octave = int(octave)
        if octave < 0 or octave > 10:
            raise ValueError("Octave must be between 0 and 10 inclusive")

        # Look up this note's frequency. (We're using a lookup table instead of
        # calculating it ourselves to avoid the inherent difficulties of
        # floating-point arithmetic and accurate precision.)
        freq = FREQ_TABLE[note][octave]

        self.note = note
        self.octave = octave
        self.freq = freq

    def __str__(self):
        if not hasattr(self, 'note'):
            return "Unknown Note"

        s = self.note
        if hasattr(self, 'octave'):
            s += str(self.octave)
        else:
            s += '?'

        return s

    def __repr__(self):
        return str(self)

    def get_harmonics(self):
        """ Get a list of harmonic frequencies for this note, ordered from
        lowest to highest, up to and including the 10th octave. The returned
        list of floats does not include this note. """

        harmonics = []

        freq = Decimal(str(self.freq * 2))
        while freq < HIGHEST_NOTE_FREQ:
            harmonics.append(freq)
            freq += self.freq

        return harmonics

    def get_octaves(self):
        """ Get a list of octave notes for this note, up to the 10th octave. The
        returned list of notes does not include this note. The notes are ordered
        from lowest to highest. """

        return [Note(self.note, octave) for octave in range(self.octave+1, 11)]


def parse_note(s):
    """ Parse the string representation of the note into a Note object. """

    result = re.fullmatch(NOTEOCTAVE_REGEX, s)
    if result is None:
        raise ValueError(f'Invalid note: "{s}"')

    # Separate the note from the octave.
    note, s = s[0], s[1:]
    if s[0] == SHARP_SYMBOL or s[0] == '#':
        note += SHARP_SYMBOL
        s = s[1:]
    elif s[0] == FLAT_SYMBOL or s[0] == 'b':
        note += FLAT_SYMBOL
        s = s[1:]
    elif s[0] == NATURAL_SYMBOL:
        s = s[1:]

    octave = int(s)

    return Note(note, octave)


def freq_to_note(freq):
    """ Return the standard note (on a 12-note scale) closest to the frequency. """

    # Make sure we're using a normalized frequency.
    freq = standardize_freq(freq)

    # Find the note for this frequency.
    for note, freqs in FREQ_TABLE.items():
        for octave, table_freq in enumerate(freqs):
            if table_freq == freq:
                return Note(note, octave)

    raise ValueError(f"Did not find note for frequency: {freq}")
