import pytest
from frequency import *


# Test the constants.
def test_consts():
    # Ensure that the reference values are correct.
    assert CONCERT_A_FREQ == Decimal('440.0000')
    assert MIDDLE_C_FREQ == Decimal('261.6256')
    assert LOWEST_NOTE_FREQ == Decimal('16.35160')
    assert HIGHEST_NOTE_FREQ == Decimal('31608.50')


# Test the function "standardize_freq".
def test_standardize_freq():
    # Test invalid frequencies.
    with pytest.raises(ValueError):
        standardize_freq(LOWEST_NOTE_FREQ - Decimal('.01'))
    with pytest.raises(ValueError):
        standardize_freq(HIGHEST_NOTE_FREQ + Decimal('.01'))

    # Test that we can nudge a note off the standard frequency and then
    # standardize it correctly.
    for _, want_freqs in FREQ_TABLE.items():
        for octave, want_freq in enumerate(want_freqs):
            perc = Decimal(str(want_freq * 2 / 100))
            if octave < 10 and octave % 2 == 0:
                test_freq = want_freq + perc
            else:
                test_freq = want_freq - perc

            freq = standardize_freq(test_freq)
            assert freq == want_freq
