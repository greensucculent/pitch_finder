from decimal import *
from notes import *

# Set the precision and rounding option for decimals.
getcontext().prec = 7
getcontext().rounding = ROUND_FLOOR


# Some standard frequencies for reference
CONCERT_A_FREQ = Decimal('440.0000')     # A4
MIDDLE_C_FREQ = Decimal('261.6256')      # C4
LOWEST_NOTE_FREQ = Decimal('16.35160')   # C0, lowest note in our range
HIGHEST_NOTE_FREQ = Decimal('31608.50')  # B10, highest note in our range


# Frequencies of all 12 notes for octaves 0-10. (Adapted from https://en.wikipedia.org/wiki/Scientific_pitch_notation)
FREQ_TABLE = {
    #            octave 0      |      octave 1      |      octave 2      |      octave 3      |      octave 4      |      octave 5      |      octave 6      |      octave 7      |      octave 8      |      octave 9      |      octave 10
    'C':  [Decimal('16.35160'), Decimal('32.70320'), Decimal('65.40639'), Decimal('130.8128'), Decimal('261.6256'), Decimal('523.2511'), Decimal('1046.502'), Decimal('2093.005'), Decimal('4186.009'), Decimal('8372.018'), Decimal('16744.04')],
    'C♯': [Decimal('17.32391'), Decimal('34.64783'), Decimal('69.29566'), Decimal('138.5913'), Decimal('277.1826'), Decimal('554.3653'), Decimal('1108.731'), Decimal('2217.461'), Decimal('4434.922'), Decimal('8869.844'), Decimal('17739.69')],
    'D':  [Decimal('18.35405'), Decimal('36.70810'), Decimal('73.41619'), Decimal('146.8324'), Decimal('293.6648'), Decimal('587.3295'), Decimal('1174.659'), Decimal('2349.318'), Decimal('4698.636'), Decimal('9397.273'), Decimal('18794.55')],
    'D♯': [Decimal('19.44544'), Decimal('38.89087'), Decimal('77.78175'), Decimal('155.5635'), Decimal('311.1270'), Decimal('622.2540'), Decimal('1244.508'), Decimal('2489.016'), Decimal('4978.032'), Decimal('9956.063'), Decimal('19912.13')],
    'E':  [Decimal('20.60172'), Decimal('41.20344'), Decimal('82.40689'), Decimal('164.8138'), Decimal('329.6276'), Decimal('659.2551'), Decimal('1318.510'), Decimal('2637.020'), Decimal('5274.041'), Decimal('10548.08'), Decimal('21096.16')],
    'F':  [Decimal('21.82676'), Decimal('43.65353'), Decimal('87.30706'), Decimal('174.6141'), Decimal('349.2282'), Decimal('698.4565'), Decimal('1396.913'), Decimal('2793.826'), Decimal('5587.652'), Decimal('11175.30'), Decimal('22350.61')],
    'F♯': [Decimal('23.12465'), Decimal('46.24930'), Decimal('92.49861'), Decimal('184.9972'), Decimal('369.9944'), Decimal('739.9888'), Decimal('1479.978'), Decimal('2959.955'), Decimal('5919.911'), Decimal('11839.82'), Decimal('23679.64')],
    'G':  [Decimal('24.49971'), Decimal('48.99943'), Decimal('97.99886'), Decimal('195.9977'), Decimal('391.9954'), Decimal('783.9909'), Decimal('1567.982'), Decimal('3135.963'), Decimal('6271.927'), Decimal('12543.85'), Decimal('25087.71')],
    'G♯': [Decimal('25.95654'), Decimal('51.91309'), Decimal('103.8262'), Decimal('207.6523'), Decimal('415.3047'), Decimal('830.6094'), Decimal('1661.219'), Decimal('3322.438'), Decimal('6644.875'), Decimal('13289.75'), Decimal('26579.50')],
    'A':  [Decimal('27.50000'), Decimal('55.00000'), Decimal('110.0000'), Decimal('220.0000'), Decimal('440.0000'), Decimal('880.0000'), Decimal('1760.000'), Decimal('3520.000'), Decimal('7040.000'), Decimal('14080.00'), Decimal('28160.00')],
    'A♯': [Decimal('29.13524'), Decimal('58.27047'), Decimal('116.5409'), Decimal('233.0819'), Decimal('466.1638'), Decimal('932.3275'), Decimal('1864.655'), Decimal('3729.310'), Decimal('7458.620'), Decimal('14917.24'), Decimal('29834.48')],
    'B':  [Decimal('30.86771'), Decimal('61.73541'), Decimal('123.4708'), Decimal('246.9417'), Decimal('493.8833'), Decimal('987.7666'), Decimal('1975.533'), Decimal('3951.066'), Decimal('7902.133'), Decimal('15804.27'), Decimal('31608.50')],
}


def standardize_freq(freq):
    """ Calculate the closest frequency that matches a note on the standard
    12-note scale. """

    freq = Decimal(freq)
    if freq < LOWEST_NOTE_FREQ or freq > HIGHEST_NOTE_FREQ:
        raise ValueError(f"Invalid frequency: {freq}")

    # Calculate the number of semitones away from Middle C (261.6256Hz) it is.
    # We're going to round this to the nearest whole number to account for
    # imperfections in the sample data.
    d = freq / MIDDLE_C_FREQ
    log = d.log10() / Decimal('2').log10()
    num_semitones = Decimal(round(12 * Decimal(log)))

    # Calculate back to a frequency, which is now based on Middle C and will
    # have a standard/normalized value.
    power = Decimal('2') ** (num_semitones/Decimal('12.0'))
    freq = MIDDLE_C_FREQ * power

    # This process of calculating a standard frequency can give slight decimal
    # value discrepancies due to the inherent difficult with floating-point
    # arithmetic. To avoid this problem, we're going to compare the calculated
    # frequency to every standard frequency in the table and use the closest
    # value by percentage.
    best = None
    chosen = Decimal('0')
    for _, freqs in FREQ_TABLE.items():
        for table_freq in freqs:
            perc = freq / table_freq * Decimal('100.0')
            diff = abs(Decimal('100.0') - round(perc))
            if best is None or diff < best:
                best = diff
                chosen = table_freq

    return chosen
