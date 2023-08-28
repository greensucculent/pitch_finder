import collections
from spectrum import *

TestFile = collections.namedtuple('TestFile', ['path', 'fund_note', 'sample_rate', 'freq_step'])

testFiles = [
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.A4.stereo.wav",  'A4',  44100, Decimal('0.3182024')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.A5.stereo.wav",  'A5',  44100, Decimal('0.3438435')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.Ab5.stereo.wav", 'G♯5', 44100, Decimal('0.4211873')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.Ab6.stereo.wav", 'G♯6', 44100, Decimal('0.4241608')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.B4.stereo.wav",  'B4',  44100, Decimal('0.3626018')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.B5.stereo.wav",  'B5',  44100, Decimal('0.4372310')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.Bb4.stereo.wav", 'A♯4', 44100, Decimal('0.3814548')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.C5.stereo.wav",  'C5',  44100, Decimal('0.3358004')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.C6.stereo.wav",  'C6',  44100, Decimal('0.4814200')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.D5.stereo.wav",  'D5',  44100, Decimal('0.3137807')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.D6.stereo.wav",  'D6',  44100, Decimal('0.3736084')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.Db5.stereo.wav", 'C♯5', 44100, Decimal('0.3671084')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.Db6.stereo.wav", 'C♯6', 44100, Decimal('0.5366138')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.E5.stereo.wav",  'E5',  44100, Decimal('0.3680889')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.E6.stereo.wav",  'E6',  44100, Decimal('0.4376563')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.Eb5.stereo.wav", 'D♯5', 44100, Decimal('0.3978420')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.Eb6.stereo.wav", 'D♯6', 44100, Decimal('0.4654599')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.F5.stereo.wav",  'F5',  44100, Decimal('0.3445312')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.F6.stereo.wav",  'F6',  44100, Decimal('0.4673986')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.G5.stereo.wav",  'G5',  44100, Decimal('0.3845214')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.G6.stereo.wav",  'G6',  44100, Decimal('0.4084770')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.Gb5.stereo.wav", 'F♯5', 44100, Decimal('0.3728693')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulA.Gb6.stereo.wav", 'F♯6', 44100, Decimal('0.3610965')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.A4.stereo.wav",  'A4',  44100, Decimal('0.3665835')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.A5.stereo.wav",  'A5',  44100, Decimal('0.6599820')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.Ab4.stereo.wav", 'G♯4', 44100, Decimal('0.4062868')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.Ab5.stereo.wav", 'G♯5', 44100, Decimal('0.6565040')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.B4.stereo.wav",  'B4',  44100, Decimal('0.5126953')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.B5.stereo.wav",  'B5',  44100, Decimal('0.5618693')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.Bb4.stereo.wav", 'A♯4', 44100, Decimal('0.4893909')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.Bb5.stereo.wav", 'A♯5', 44100, Decimal('0.7127733')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.C5.stereo.wav",  'C5',  44100, Decimal('0.5503694')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.C6.stereo.wav",  'C6',  44100, Decimal('0.6364003')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.D4.stereo.wav",  'D4',  44100, Decimal('0.2132124')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.D5.stereo.wav",  'D5',  44100, Decimal('0.3079888')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.Db5.stereo.wav", 'C♯5', 44100, Decimal('0.5417158')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.E4.stereo.wav",  'E4',  44100, Decimal('0.3466654')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.E5.stereo.wav",  'E5',  44100, Decimal('0.3838019')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.Eb4.stereo.wav", 'D♯4', 44100, Decimal('0.2814797')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.Eb5.stereo.wav", 'D♯5', 44100, Decimal('0.5644149')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.F4.stereo.wav",  'F4',  44100, Decimal('0.3744904')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.F5.stereo.wav",  'F5',  44100, Decimal('0.6236829')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.G4.stereo.wav",  'G4',  44100, Decimal('0.3680889')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.G5.stereo.wav",  'G5',  44100, Decimal('0.5856107')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulD.Gb5.stereo.wav", 'F♯5', 44100, Decimal('0.7252096')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.A5.stereo.wav",  'A5',  44100, Decimal('0.4989421')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.A6.stereo.wav",  'A6',  44100, Decimal('0.3087521')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.Ab5.stereo.wav", 'G♯5', 44100, Decimal('0.9308707')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.Ab6.stereo.wav", 'G♯6', 44100, Decimal('0.3012933')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.B5.stereo.wav",  'B5',  44100, Decimal('0.7796064')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.B6.stereo.wav",  'B6',  44100, Decimal('0.3012933')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.Bb5.stereo.wav", 'A♯5', 44100, Decimal('0.7894595')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.Bb6.stereo.wav", 'A♯6', 44100, Decimal('0.3012933')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.C6.stereo.wav",  'C6',  44100, Decimal('0.2747492')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.C7.stereo.wav",  'C7',  44100, Decimal('1.299313')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.D7.stereo.wav",  'D7',  44100, Decimal('0.7605808')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.Db6.stereo.wav", 'C♯6', 44100, Decimal('0.2699906')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.Db7.stereo.wav", 'C♯7', 44100, Decimal('1.052631')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.E5.stereo.wav",  'E5',  44100, Decimal('0.4171711')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.E6.stereo.wav",  'E6',  44100, Decimal('0.3064756')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.E7.stereo.wav",  'E7',  44100, Decimal('0.7148182')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.Eb7.stereo.wav", 'D♯7', 44100, Decimal('1.334059')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.F5.stereo.wav",  'F5',  44100, Decimal('0.5695687')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.F6.stereo.wav",  'F6',  44100, Decimal('0.2854368')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.G5.stereo.wav",  'G5',  44100, Decimal('0.4891575')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.G6.stereo.wav",  'G6',  44100, Decimal('0.3299885')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.Gb5.stereo.wav", 'F♯5', 44100, Decimal('0.5828784')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulE.Gb6.stereo.wav", 'F♯6', 44100, Decimal('0.2867472')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulG.A3.stereo.wav",  'A3',  44100, Decimal('0.3674112')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulG.A4.stereo.wav",  'A4',  44100, Decimal('0.2682498')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulG.Ab3.stereo.wav", 'G♯3', 44100, Decimal('0.3592112')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulG.Ab4.stereo.wav", 'G♯4', 44100, Decimal('0.6055197')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulG.B3.stereo.wav",  'B3',  44100, Decimal('0.3701341')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulG.B4.stereo.wav",  'B4',  44100, Decimal('0.4454860')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulG.Bb3.stereo.wav", 'A♯3', 44100, Decimal('0.4853514')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulG.Bb4.stereo.wav", 'A♯4', 44100, Decimal('0.5695687')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulG.C4.stereo.wav",  'C4',  44100, Decimal('0.3861781')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulG.C5.stereo.wav",  'C5',  44100, Decimal('0.4585868')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulG.D4.stereo.wav",  'D4',  44100, Decimal('0.1916058')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulG.D5.stereo.wav",  'D5',  44100, Decimal('0.4533305')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulG.Db4.stereo.wav", 'C♯4', 44100, Decimal('0.4316124')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulG.Db5.stereo.wav", 'C♯5', 44100, Decimal('0.4910858')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulG.E4.stereo.wav",  'E4',  44100, Decimal('0.4271765')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulG.Eb4.stereo.wav", 'D♯4', 44100, Decimal('0.4116686')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulG.F4.stereo.wav",  'F4',  44100, Decimal('0.4331087')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulG.G3.stereo.wav",  'G3',  44100, Decimal('0.2340255')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulG.G4.stereo.wav",  'G4',  44100, Decimal('0.4671758')),
    TestFile("samples/mis/violin/Violin.arco.ff.sulG.Gb4.stereo.wav", 'F♯4', 44100, Decimal('0.3791363'))
]


# Test creating new Spectrum objects.
def test_Spectrum():
    for testFile in testFiles:
        spectrum = Spectrum(testFile.path)
        assert testFile.path == spectrum.path
        assert testFile.sample_rate == spectrum.sample_rate
        assert testFile.freq_step == spectrum.freq_step


# Test the "get_fund_note" method for Spectrum objects.
def test_Spectrum_get_fund_note():
    for testFile in testFiles:
        spectrum = Spectrum(testFile.path)
        fund_freq = spectrum.get_fund_freq()
        note = freq_to_note(fund_freq)
        assert testFile.fund_note == str(note)
