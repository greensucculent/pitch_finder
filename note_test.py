import pytest
from note import *


# Test that the global constants have the correct values.
def test_constants():
    # Ensure that the symbols are correct.
    assert SHARP_SYMBOL == '♯'
    assert SHARP_SYMBOL_ALT == '#'
    assert FLAT_SYMBOL == '♭'
    assert FLAT_SYMBOL_ALT == 'b'
    assert NATURAL_SYMBOL == '♮'

    # Ensure that these constants have the correct values.
    assert C_NOTE == 'C'
    assert CSHARP_NOTE == 'C♯'
    assert D_NOTE == 'D'
    assert DSHARP_NOTE == 'D♯'
    assert E_NOTE == 'E'
    assert F_NOTE == 'F'
    assert FSHARP_NOTE == 'F♯'
    assert G_NOTE == 'G'
    assert GSHARP_NOTE == 'G♯'
    assert A_NOTE == 'A'
    assert ASHARP_NOTE == 'A♯'
    assert B_NOTE == 'B'

    # Ensure that the ordered list of notes is correct.
    assert len(NOTES) == 12
    assert NOTES[0] == 'C'
    assert NOTES[1] == 'C♯'
    assert NOTES[2] == 'D'
    assert NOTES[3] == 'D♯'
    assert NOTES[4] == 'E'
    assert NOTES[5] == 'F'
    assert NOTES[6] == 'F♯'
    assert NOTES[7] == 'G'
    assert NOTES[8] == 'G♯'
    assert NOTES[9] == 'A'
    assert NOTES[10] == 'A♯'
    assert NOTES[11] == 'B'


# Test initializing new Note objects.
def test_Note():
    # Test no value.
    with pytest.raises(ValueError):
        Note('', 1)

    # Test a long note.
    with pytest.raises(ValueError):
        Note('C♯NNN', 1)

    # Test an invalid note.
    with pytest.raises(ValueError):
        Note('Dc5', 1)

    # Test a bogus note.
    with pytest.raises(ValueError):
        Note('bogus', 5)

    # Test a negative octave.
    with pytest.raises(ValueError):
        Note('C', -1)

    # Test an octave that's too high.
    with pytest.raises(ValueError):
        Note('C', 11)

    # Test an octave that's a string instead of an integer.
    note = Note('C', '5')
    assert note.note == 'C'
    assert note.octave == 5
    assert note.freq == Decimal('523.2511')
    assert str(note.freq) == '523.2511'
    assert str(note) == 'C5'

    # Test an octave that's an invalid string instead of an integer.
    with pytest.raises(ValueError):
        Note('C', 'aaa')

    # Test an octave that's a float instead of an integer.
    note = Note('F♯', 3.3)
    assert note.note == 'F♯'
    assert note.octave == 3
    assert note.freq == Decimal('184.9972')
    assert str(note.freq) == '184.9972'
    assert str(note) == 'F♯3'

    # Test expected note values.
    for want_note in NOTES:
        for want_octave in range(0, 11):
            note = Note(want_note, want_octave)
            assert str(note) == f'{want_note}{want_octave}'
            assert note.note == want_note
            assert note.octave == want_octave

    # Test alternative sharp symbols.
    for want_note in NOTES:
        for want_octave in range(0, 11):
            use_note = want_note
            if len(use_note) == 2 and use_note[1] == SHARP_SYMBOL:
                use_note = use_note[0] + '#'
            note = Note(use_note, want_octave)
            assert str(note) == f'{want_note}{want_octave}'
            assert note.note == want_note
            assert note.octave == want_octave

    # Test valid flat symbols.
    note = Note(f'D{FLAT_SYMBOL}', 3)
    assert str(note) == f'C{SHARP_SYMBOL}3'
    note = Note(f'E{FLAT_SYMBOL}', 3)
    assert str(note) == f'D{SHARP_SYMBOL}3'
    note = Note(f'G{FLAT_SYMBOL}', 3)
    assert str(note) == f'F{SHARP_SYMBOL}3'
    note = Note(f'A{FLAT_SYMBOL}', 3)
    assert str(note) == f'G{SHARP_SYMBOL}3'
    note = Note(f'B{FLAT_SYMBOL}', 3)
    assert str(note) == f'A{SHARP_SYMBOL}3'

    # Test alternative flat symbols.
    note = Note(f'Db', 3)
    assert str(note) == f'C{SHARP_SYMBOL}3'
    note = Note(f'Eb', 3)
    assert str(note) == f'D{SHARP_SYMBOL}3'
    note = Note(f'Gb', 3)
    assert str(note) == f'F{SHARP_SYMBOL}3'
    note = Note(f'Ab', 3)
    assert str(note) == f'G{SHARP_SYMBOL}3'
    note = Note(f'Bb', 3)
    assert str(note) == f'A{SHARP_SYMBOL}3'

    # Test invalid flat symbols.
    with pytest.raises(KeyError):
        Note(f'C{FLAT_SYMBOL}', 4)
    with pytest.raises(KeyError):
        Note(f'Cb', 4)
    with pytest.raises(KeyError):
        Note(f'F{FLAT_SYMBOL}', 4)
    with pytest.raises(KeyError):
        Note(f'Fb', 4)

    # Test natural symbols.
    note = Note(f'C{NATURAL_SYMBOL}', 6)
    assert str(note) == 'C6'
    note = Note(f'D{NATURAL_SYMBOL}', 6)
    assert str(note) == 'D6'
    note = Note(f'E{NATURAL_SYMBOL}', 6)
    assert str(note) == 'E6'
    note = Note(f'F{NATURAL_SYMBOL}', 6)
    assert str(note) == 'F6'
    note = Note(f'G{NATURAL_SYMBOL}', 6)
    assert str(note) == 'G6'
    note = Note(f'A{NATURAL_SYMBOL}', 6)
    assert str(note) == 'A6'
    note = Note(f'B{NATURAL_SYMBOL}', 6)
    assert str(note) == 'B6'

    # Test that every note in every octave has the correct frequency.
    for want_note, want_freqs in FREQ_TABLE.items():
        for want_octave, want_freq in enumerate(want_freqs):
            note = Note(want_note, want_octave)
            assert note.note == want_note
            assert note.octave == want_octave
            assert note.freq == want_freq
            assert str(note.freq) == str(want_freq)
            assert str(note) == f'{want_note}{want_octave}'


# Test the "get_harmonics" method for Note objects.
def test_Note_get_harmonics():
    # Test the harmonics for C5.
    want_harmonics = [
        Decimal('1046.502'), Decimal('1569.753'), Decimal('2093.004'), Decimal('2616.255'), Decimal('3139.506'),
        Decimal('3662.757'), Decimal('4186.008'), Decimal('4709.259'), Decimal('5232.510'), Decimal('5755.761'),
        Decimal('6279.012'), Decimal('6802.263'), Decimal('7325.514'), Decimal('7848.765'), Decimal('8372.016'),
        Decimal('8895.267'), Decimal('9418.518'), Decimal('9941.769'), Decimal('10465.02'), Decimal('10988.27'),
        Decimal('11511.52'), Decimal('12034.77'), Decimal('12558.02'), Decimal('13081.27'), Decimal('13604.52'),
        Decimal('14127.77'), Decimal('14651.02'), Decimal('15174.27'), Decimal('15697.52'), Decimal('16220.77'),
        Decimal('16744.02'), Decimal('17267.27'), Decimal('17790.52'), Decimal('18313.77'), Decimal('18837.02'),
        Decimal('19360.27'), Decimal('19883.52'), Decimal('20406.77'), Decimal('20930.02'), Decimal('21453.27'),
        Decimal('21976.52'), Decimal('22499.77'), Decimal('23023.02'), Decimal('23546.27'), Decimal('24069.52'),
        Decimal('24592.77'), Decimal('25116.02'), Decimal('25639.27'), Decimal('26162.52'), Decimal('26685.77'),
        Decimal('27209.02'), Decimal('27732.27'), Decimal('28255.52'), Decimal('28778.77'), Decimal('29302.02'),
        Decimal('29825.27'), Decimal('30348.52'), Decimal('30871.77'), Decimal('31395.02')
    ]
    note = Note('C', 5)
    harmonics = note.get_harmonics()
    assert len(harmonics) == len(want_harmonics)
    for i, harmonic in enumerate(harmonics):
        assert type(harmonic) == Decimal
        assert harmonic == want_harmonics[i]

    # Test the harmonics for G♯8.
    want_harmonics = [Decimal('13289.75'), Decimal('19934.62'), Decimal('26579.49')]
    note = Note('G♯', 8)
    harmonics = note.get_harmonics()
    assert len(harmonics) == len(want_harmonics)
    for i, harmonic in enumerate(harmonics):
        assert type(harmonic) == Decimal
        assert harmonic == want_harmonics[i]

    # Test the harmonics for the lowest note.
    want_harmonics = [
        Decimal('32.70320'), Decimal('49.05480'), Decimal('65.40640'), Decimal('81.75800'), Decimal('98.10960'), Decimal('114.4612'), Decimal('130.8128'), Decimal('147.1644'), Decimal('163.5160'), Decimal('179.8676'), Decimal('196.2192'), Decimal('212.5708'), Decimal(
            '228.9224'), Decimal('245.2740'), Decimal('261.6256'), Decimal('277.9772'), Decimal('294.3288'), Decimal('310.6804'), Decimal('327.0320'), Decimal('343.3836'), Decimal('359.7352'), Decimal('376.0868'), Decimal('392.4384'), Decimal('408.7900'),
        Decimal('425.1416'), Decimal('441.4932'), Decimal('457.8448'), Decimal('474.1964'), Decimal('490.5480'), Decimal('506.8996'), Decimal('523.2512'), Decimal('539.6028'), Decimal('555.9544'), Decimal('572.3060'), Decimal('588.6576'), Decimal('605.0092'), Decimal(
            '621.3608'), Decimal('637.7124'), Decimal('654.0640'), Decimal('670.4156'), Decimal('686.7672'), Decimal('703.1188'), Decimal('719.4704'), Decimal('735.8220'), Decimal('752.1736'), Decimal('768.5252'), Decimal('784.8768'), Decimal('801.2284'), Decimal('817.5800'),
        Decimal('833.9316'), Decimal('850.2832'), Decimal('866.6348'), Decimal('882.9864'), Decimal('899.3380'), Decimal('915.6896'), Decimal('932.0412'), Decimal('948.3928'), Decimal('964.7444'), Decimal('981.0960'), Decimal('997.4476'), Decimal('1013.799'), Decimal('1030.150'), Decimal('1046.501'), Decimal('1062.852'), Decimal('1079.203'), Decimal('1095.554'), Decimal('1111.905'), Decimal('1128.256'), Decimal('1144.607'), Decimal('1160.958'), Decimal('1177.309'), Decimal('1193.660'), Decimal('1210.011'), Decimal(
            '1226.362'), Decimal('1242.713'), Decimal('1259.064'), Decimal('1275.415'), Decimal('1291.766'), Decimal('1308.117'), Decimal('1324.468'), Decimal('1340.819'), Decimal('1357.170'), Decimal('1373.521'), Decimal('1389.872'), Decimal('1406.223'), Decimal('1422.574'), Decimal('1438.925'), Decimal('1455.276'), Decimal('1471.627'), Decimal('1487.978'), Decimal('1504.329'), Decimal('1520.680'), Decimal('1537.031'), Decimal('1553.382'), Decimal('1569.733'), Decimal('1586.084'), Decimal('1602.435'), Decimal('1618.786'),
        Decimal('1635.137'), Decimal('1651.488'), Decimal('1667.839'), Decimal('1684.190'), Decimal('1700.541'), Decimal('1716.892'), Decimal('1733.243'), Decimal('1749.594'), Decimal('1765.945'), Decimal('1782.296'), Decimal('1798.647'), Decimal('1814.998'), Decimal('1831.349'), Decimal('1847.700'), Decimal('1864.051'), Decimal('1880.402'), Decimal('1896.753'), Decimal('1913.104'), Decimal('1929.455'), Decimal('1945.806'), Decimal('1962.157'), Decimal('1978.508'), Decimal('1994.859'), Decimal('2011.210'), Decimal(
            '2027.561'), Decimal('2043.912'), Decimal('2060.263'), Decimal('2076.614'), Decimal('2092.965'), Decimal('2109.316'), Decimal('2125.667'), Decimal('2142.018'), Decimal('2158.369'), Decimal('2174.720'), Decimal('2191.071'), Decimal('2207.422'), Decimal('2223.773'), Decimal('2240.124'), Decimal('2256.475'), Decimal('2272.826'), Decimal('2289.177'), Decimal('2305.528'), Decimal('2321.879'), Decimal('2338.230'), Decimal('2354.581'), Decimal('2370.932'), Decimal('2387.283'), Decimal('2403.634'), Decimal('2419.985'),
        Decimal('2436.336'), Decimal('2452.687'), Decimal('2469.038'), Decimal('2485.389'), Decimal('2501.740'), Decimal('2518.091'), Decimal('2534.442'), Decimal('2550.793'), Decimal('2567.144'), Decimal('2583.495'), Decimal('2599.846'), Decimal('2616.197'), Decimal('2632.548'), Decimal('2648.899'), Decimal('2665.250'), Decimal('2681.601'), Decimal('2697.952'), Decimal('2714.303'), Decimal('2730.654'), Decimal('2747.005'), Decimal('2763.356'), Decimal('2779.707'), Decimal('2796.058'), Decimal('2812.409'), Decimal(
            '2828.760'), Decimal('2845.111'), Decimal('2861.462'), Decimal('2877.813'), Decimal('2894.164'), Decimal('2910.515'), Decimal('2926.866'), Decimal('2943.217'), Decimal('2959.568'), Decimal('2975.919'), Decimal('2992.270'), Decimal('3008.621'), Decimal('3024.972'), Decimal('3041.323'), Decimal('3057.674'), Decimal('3074.025'), Decimal('3090.376'), Decimal('3106.727'), Decimal('3123.078'), Decimal('3139.429'), Decimal('3155.780'), Decimal('3172.131'), Decimal('3188.482'), Decimal('3204.833'), Decimal('3221.184'),
        Decimal('3237.535'), Decimal('3253.886'), Decimal('3270.237'), Decimal('3286.588'), Decimal('3302.939'), Decimal('3319.290'), Decimal('3335.641'), Decimal('3351.992'), Decimal('3368.343'), Decimal('3384.694'), Decimal('3401.045'), Decimal('3417.396'), Decimal('3433.747'), Decimal('3450.098'), Decimal('3466.449'), Decimal('3482.800'), Decimal('3499.151'), Decimal('3515.502'), Decimal('3531.853'), Decimal('3548.204'), Decimal('3564.555'), Decimal('3580.906'), Decimal('3597.257'), Decimal('3613.608'), Decimal(
            '3629.959'), Decimal('3646.310'), Decimal('3662.661'), Decimal('3679.012'), Decimal('3695.363'), Decimal('3711.714'), Decimal('3728.065'), Decimal('3744.416'), Decimal('3760.767'), Decimal('3777.118'), Decimal('3793.469'), Decimal('3809.820'), Decimal('3826.171'), Decimal('3842.522'), Decimal('3858.873'), Decimal('3875.224'), Decimal('3891.575'), Decimal('3907.926'), Decimal('3924.277'), Decimal('3940.628'), Decimal('3956.979'), Decimal('3973.330'), Decimal('3989.681'), Decimal('4006.032'), Decimal('4022.383'),
        Decimal('4038.734'), Decimal('4055.085'), Decimal('4071.436'), Decimal('4087.787'), Decimal('4104.138'), Decimal('4120.489'), Decimal('4136.840'), Decimal('4153.191'), Decimal('4169.542'), Decimal('4185.893'), Decimal('4202.244'), Decimal('4218.595'), Decimal('4234.946'), Decimal('4251.297'), Decimal('4267.648'), Decimal('4283.999'), Decimal('4300.350'), Decimal('4316.701'), Decimal('4333.052'), Decimal('4349.403'), Decimal('4365.754'), Decimal('4382.105'), Decimal('4398.456'), Decimal('4414.807'), Decimal(
            '4431.158'), Decimal('4447.509'), Decimal('4463.860'), Decimal('4480.211'), Decimal('4496.562'), Decimal('4512.913'), Decimal('4529.264'), Decimal('4545.615'), Decimal('4561.966'), Decimal('4578.317'), Decimal('4594.668'), Decimal('4611.019'), Decimal('4627.370'), Decimal('4643.721'), Decimal('4660.072'), Decimal('4676.423'), Decimal('4692.774'), Decimal('4709.125'), Decimal('4725.476'), Decimal('4741.827'), Decimal('4758.178'), Decimal('4774.529'), Decimal('4790.880'), Decimal('4807.231'), Decimal('4823.582'),
        Decimal('4839.933'), Decimal('4856.284'), Decimal('4872.635'), Decimal('4888.986'), Decimal('4905.337'), Decimal('4921.688'), Decimal('4938.039'), Decimal('4954.390'), Decimal('4970.741'), Decimal('4987.092'), Decimal('5003.443'), Decimal('5019.794'), Decimal('5036.145'), Decimal('5052.496'), Decimal('5068.847'), Decimal('5085.198'), Decimal('5101.549'), Decimal('5117.900'), Decimal('5134.251'), Decimal('5150.602'), Decimal('5166.953'), Decimal('5183.304'), Decimal('5199.655'), Decimal('5216.006'), Decimal(
            '5232.357'), Decimal('5248.708'), Decimal('5265.059'), Decimal('5281.410'), Decimal('5297.761'), Decimal('5314.112'), Decimal('5330.463'), Decimal('5346.814'), Decimal('5363.165'), Decimal('5379.516'), Decimal('5395.867'), Decimal('5412.218'), Decimal('5428.569'), Decimal('5444.920'), Decimal('5461.271'), Decimal('5477.622'), Decimal('5493.973'), Decimal('5510.324'), Decimal('5526.675'), Decimal('5543.026'), Decimal('5559.377'), Decimal('5575.728'), Decimal('5592.079'), Decimal('5608.430'), Decimal('5624.781'),
        Decimal('5641.132'), Decimal('5657.483'), Decimal('5673.834'), Decimal('5690.185'), Decimal('5706.536'), Decimal('5722.887'), Decimal('5739.238'), Decimal('5755.589'), Decimal('5771.940'), Decimal('5788.291'), Decimal('5804.642'), Decimal('5820.993'), Decimal('5837.344'), Decimal('5853.695'), Decimal('5870.046'), Decimal('5886.397'), Decimal('5902.748'), Decimal('5919.099'), Decimal('5935.450'), Decimal('5951.801'), Decimal('5968.152'), Decimal('5984.503'), Decimal('6000.854'), Decimal('6017.205'), Decimal(
            '6033.556'), Decimal('6049.907'), Decimal('6066.258'), Decimal('6082.609'), Decimal('6098.960'), Decimal('6115.311'), Decimal('6131.662'), Decimal('6148.013'), Decimal('6164.364'), Decimal('6180.715'), Decimal('6197.066'), Decimal('6213.417'), Decimal('6229.768'), Decimal('6246.119'), Decimal('6262.470'), Decimal('6278.821'), Decimal('6295.172'), Decimal('6311.523'), Decimal('6327.874'), Decimal('6344.225'), Decimal('6360.576'), Decimal('6376.927'), Decimal('6393.278'), Decimal('6409.629'), Decimal('6425.980'),
        Decimal('6442.331'), Decimal('6458.682'), Decimal('6475.033'), Decimal('6491.384'), Decimal('6507.735'), Decimal('6524.086'), Decimal('6540.437'), Decimal('6556.788'), Decimal('6573.139'), Decimal('6589.490'), Decimal('6605.841'), Decimal('6622.192'), Decimal('6638.543'), Decimal('6654.894'), Decimal('6671.245'), Decimal('6687.596'), Decimal('6703.947'), Decimal('6720.298'), Decimal('6736.649'), Decimal('6753.000'), Decimal('6769.351'), Decimal('6785.702'), Decimal('6802.053'), Decimal('6818.404'), Decimal(
            '6834.755'), Decimal('6851.106'), Decimal('6867.457'), Decimal('6883.808'), Decimal('6900.159'), Decimal('6916.510'), Decimal('6932.861'), Decimal('6949.212'), Decimal('6965.563'), Decimal('6981.914'), Decimal('6998.265'), Decimal('7014.616'), Decimal('7030.967'), Decimal('7047.318'), Decimal('7063.669'), Decimal('7080.020'), Decimal('7096.371'), Decimal('7112.722'), Decimal('7129.073'), Decimal('7145.424'), Decimal('7161.775'), Decimal('7178.126'), Decimal('7194.477'), Decimal('7210.828'), Decimal('7227.179'),
        Decimal('7243.530'), Decimal('7259.881'), Decimal('7276.232'), Decimal('7292.583'), Decimal('7308.934'), Decimal('7325.285'), Decimal('7341.636'), Decimal('7357.987'), Decimal('7374.338'), Decimal('7390.689'), Decimal('7407.040'), Decimal('7423.391'), Decimal('7439.742'), Decimal('7456.093'), Decimal('7472.444'), Decimal('7488.795'), Decimal('7505.146'), Decimal('7521.497'), Decimal('7537.848'), Decimal('7554.199'), Decimal('7570.550'), Decimal('7586.901'), Decimal('7603.252'), Decimal('7619.603'), Decimal(
            '7635.954'), Decimal('7652.305'), Decimal('7668.656'), Decimal('7685.007'), Decimal('7701.358'), Decimal('7717.709'), Decimal('7734.060'), Decimal('7750.411'), Decimal('7766.762'), Decimal('7783.113'), Decimal('7799.464'), Decimal('7815.815'), Decimal('7832.166'), Decimal('7848.517'), Decimal('7864.868'), Decimal('7881.219'), Decimal('7897.570'), Decimal('7913.921'), Decimal('7930.272'), Decimal('7946.623'), Decimal('7962.974'), Decimal('7979.325'), Decimal('7995.676'), Decimal('8012.027'), Decimal('8028.378'),
        Decimal('8044.729'), Decimal('8061.080'), Decimal('8077.431'), Decimal('8093.782'), Decimal('8110.133'), Decimal('8126.484'), Decimal('8142.835'), Decimal('8159.186'), Decimal('8175.537'), Decimal('8191.888'), Decimal('8208.239'), Decimal('8224.590'), Decimal('8240.941'), Decimal('8257.292'), Decimal('8273.643'), Decimal('8289.994'), Decimal('8306.345'), Decimal('8322.696'), Decimal('8339.047'), Decimal('8355.398'), Decimal('8371.749'), Decimal('8388.100'), Decimal('8404.451'), Decimal('8420.802'), Decimal(
            '8437.153'), Decimal('8453.504'), Decimal('8469.855'), Decimal('8486.206'), Decimal('8502.557'), Decimal('8518.908'), Decimal('8535.259'), Decimal('8551.610'), Decimal('8567.961'), Decimal('8584.312'), Decimal('8600.663'), Decimal('8617.014'), Decimal('8633.365'), Decimal('8649.716'), Decimal('8666.067'), Decimal('8682.418'), Decimal('8698.769'), Decimal('8715.120'), Decimal('8731.471'), Decimal('8747.822'), Decimal('8764.173'), Decimal('8780.524'), Decimal('8796.875'), Decimal('8813.226'), Decimal('8829.577'),
        Decimal('8845.928'), Decimal('8862.279'), Decimal('8878.630'), Decimal('8894.981'), Decimal('8911.332'), Decimal('8927.683'), Decimal('8944.034'), Decimal('8960.385'), Decimal('8976.736'), Decimal('8993.087'), Decimal('9009.438'), Decimal('9025.789'), Decimal('9042.140'), Decimal('9058.491'), Decimal('9074.842'), Decimal('9091.193'), Decimal('9107.544'), Decimal('9123.895'), Decimal('9140.246'), Decimal('9156.597'), Decimal('9172.948'), Decimal('9189.299'), Decimal('9205.650'), Decimal('9222.001'), Decimal(
            '9238.352'), Decimal('9254.703'), Decimal('9271.054'), Decimal('9287.405'), Decimal('9303.756'), Decimal('9320.107'), Decimal('9336.458'), Decimal('9352.809'), Decimal('9369.160'), Decimal('9385.511'), Decimal('9401.862'), Decimal('9418.213'), Decimal('9434.564'), Decimal('9450.915'), Decimal('9467.266'), Decimal('9483.617'), Decimal('9499.968'), Decimal('9516.319'), Decimal('9532.670'), Decimal('9549.021'), Decimal('9565.372'), Decimal('9581.723'), Decimal('9598.074'), Decimal('9614.425'), Decimal('9630.776'),
        Decimal('9647.127'), Decimal('9663.478'), Decimal('9679.829'), Decimal('9696.180'), Decimal('9712.531'), Decimal('9728.882'), Decimal('9745.233'), Decimal('9761.584'), Decimal('9777.935'), Decimal('9794.286'), Decimal('9810.637'), Decimal('9826.988'), Decimal('9843.339'), Decimal('9859.690'), Decimal('9876.041'), Decimal('9892.392'), Decimal('9908.743'), Decimal('9925.094'), Decimal('9941.445'), Decimal('9957.796'), Decimal('9974.147'), Decimal('9990.498'), Decimal('10006.84'), Decimal('10023.19'), Decimal(
            '10039.54'), Decimal('10055.89'), Decimal('10072.24'), Decimal('10088.59'), Decimal('10104.94'), Decimal('10121.29'), Decimal('10137.64'), Decimal('10153.99'), Decimal('10170.34'), Decimal('10186.69'), Decimal('10203.04'), Decimal('10219.39'), Decimal('10235.74'), Decimal('10252.09'), Decimal('10268.44'), Decimal('10284.79'), Decimal('10301.14'), Decimal('10317.49'), Decimal('10333.84'), Decimal('10350.19'), Decimal('10366.54'), Decimal('10382.89'), Decimal('10399.24'), Decimal('10415.59'), Decimal('10431.94'),
        Decimal('10448.29'), Decimal('10464.64'), Decimal('10480.99'), Decimal('10497.34'), Decimal('10513.69'), Decimal('10530.04'), Decimal('10546.39'), Decimal('10562.74'), Decimal('10579.09'), Decimal('10595.44'), Decimal('10611.79'), Decimal('10628.14'), Decimal('10644.49'), Decimal('10660.84'), Decimal('10677.19'), Decimal('10693.54'), Decimal('10709.89'), Decimal('10726.24'), Decimal('10742.59'), Decimal('10758.94'), Decimal('10775.29'), Decimal('10791.64'), Decimal('10807.99'), Decimal('10824.34'), Decimal(
            '10840.69'), Decimal('10857.04'), Decimal('10873.39'), Decimal('10889.74'), Decimal('10906.09'), Decimal('10922.44'), Decimal('10938.79'), Decimal('10955.14'), Decimal('10971.49'), Decimal('10987.84'), Decimal('11004.19'), Decimal('11020.54'), Decimal('11036.89'), Decimal('11053.24'), Decimal('11069.59'), Decimal('11085.94'), Decimal('11102.29'), Decimal('11118.64'), Decimal('11134.99'), Decimal('11151.34'), Decimal('11167.69'), Decimal('11184.04'), Decimal('11200.39'), Decimal('11216.74'), Decimal('11233.09'),
        Decimal('11249.44'), Decimal('11265.79'), Decimal('11282.14'), Decimal('11298.49'), Decimal('11314.84'), Decimal('11331.19'), Decimal('11347.54'), Decimal('11363.89'), Decimal('11380.24'), Decimal('11396.59'), Decimal('11412.94'), Decimal('11429.29'), Decimal('11445.64'), Decimal('11461.99'), Decimal('11478.34'), Decimal('11494.69'), Decimal('11511.04'), Decimal('11527.39'), Decimal('11543.74'), Decimal('11560.09'), Decimal('11576.44'), Decimal('11592.79'), Decimal('11609.14'), Decimal('11625.49'), Decimal(
            '11641.84'), Decimal('11658.19'), Decimal('11674.54'), Decimal('11690.89'), Decimal('11707.24'), Decimal('11723.59'), Decimal('11739.94'), Decimal('11756.29'), Decimal('11772.64'), Decimal('11788.99'), Decimal('11805.34'), Decimal('11821.69'), Decimal('11838.04'), Decimal('11854.39'), Decimal('11870.74'), Decimal('11887.09'), Decimal('11903.44'), Decimal('11919.79'), Decimal('11936.14'), Decimal('11952.49'), Decimal('11968.84'), Decimal('11985.19'), Decimal('12001.54'), Decimal('12017.89'), Decimal('12034.24'),
        Decimal('12050.59'), Decimal('12066.94'), Decimal('12083.29'), Decimal('12099.64'), Decimal('12115.99'), Decimal('12132.34'), Decimal('12148.69'), Decimal('12165.04'), Decimal('12181.39'), Decimal('12197.74'), Decimal('12214.09'), Decimal('12230.44'), Decimal('12246.79'), Decimal('12263.14'), Decimal('12279.49'), Decimal('12295.84'), Decimal('12312.19'), Decimal('12328.54'), Decimal('12344.89'), Decimal('12361.24'), Decimal('12377.59'), Decimal('12393.94'), Decimal('12410.29'), Decimal('12426.64'), Decimal(
            '12442.99'), Decimal('12459.34'), Decimal('12475.69'), Decimal('12492.04'), Decimal('12508.39'), Decimal('12524.74'), Decimal('12541.09'), Decimal('12557.44'), Decimal('12573.79'), Decimal('12590.14'), Decimal('12606.49'), Decimal('12622.84'), Decimal('12639.19'), Decimal('12655.54'), Decimal('12671.89'), Decimal('12688.24'), Decimal('12704.59'), Decimal('12720.94'), Decimal('12737.29'), Decimal('12753.64'), Decimal('12769.99'), Decimal('12786.34'), Decimal('12802.69'), Decimal('12819.04'), Decimal('12835.39'),
        Decimal('12851.74'), Decimal('12868.09'), Decimal('12884.44'), Decimal('12900.79'), Decimal('12917.14'), Decimal('12933.49'), Decimal('12949.84'), Decimal('12966.19'), Decimal('12982.54'), Decimal('12998.89'), Decimal('13015.24'), Decimal('13031.59'), Decimal('13047.94'), Decimal('13064.29'), Decimal('13080.64'), Decimal('13096.99'), Decimal('13113.34'), Decimal('13129.69'), Decimal('13146.04'), Decimal('13162.39'), Decimal('13178.74'), Decimal('13195.09'), Decimal('13211.44'), Decimal('13227.79'), Decimal(
            '13244.14'), Decimal('13260.49'), Decimal('13276.84'), Decimal('13293.19'), Decimal('13309.54'), Decimal('13325.89'), Decimal('13342.24'), Decimal('13358.59'), Decimal('13374.94'), Decimal('13391.29'), Decimal('13407.64'), Decimal('13423.99'), Decimal('13440.34'), Decimal('13456.69'), Decimal('13473.04'), Decimal('13489.39'), Decimal('13505.74'), Decimal('13522.09'), Decimal('13538.44'), Decimal('13554.79'), Decimal('13571.14'), Decimal('13587.49'), Decimal('13603.84'), Decimal('13620.19'), Decimal('13636.54'),
        Decimal('13652.89'), Decimal('13669.24'), Decimal('13685.59'), Decimal('13701.94'), Decimal('13718.29'), Decimal('13734.64'), Decimal('13750.99'), Decimal('13767.34'), Decimal('13783.69'), Decimal('13800.04'), Decimal('13816.39'), Decimal('13832.74'), Decimal('13849.09'), Decimal('13865.44'), Decimal('13881.79'), Decimal('13898.14'), Decimal('13914.49'), Decimal('13930.84'), Decimal('13947.19'), Decimal('13963.54'), Decimal('13979.89'), Decimal('13996.24'), Decimal('14012.59'), Decimal('14028.94'), Decimal(
            '14045.29'), Decimal('14061.64'), Decimal('14077.99'), Decimal('14094.34'), Decimal('14110.69'), Decimal('14127.04'), Decimal('14143.39'), Decimal('14159.74'), Decimal('14176.09'), Decimal('14192.44'), Decimal('14208.79'), Decimal('14225.14'), Decimal('14241.49'), Decimal('14257.84'), Decimal('14274.19'), Decimal('14290.54'), Decimal('14306.89'), Decimal('14323.24'), Decimal('14339.59'), Decimal('14355.94'), Decimal('14372.29'), Decimal('14388.64'), Decimal('14404.99'), Decimal('14421.34'), Decimal('14437.69'),
        Decimal('14454.04'), Decimal('14470.39'), Decimal('14486.74'), Decimal('14503.09'), Decimal('14519.44'), Decimal('14535.79'), Decimal('14552.14'), Decimal('14568.49'), Decimal('14584.84'), Decimal('14601.19'), Decimal('14617.54'), Decimal('14633.89'), Decimal('14650.24'), Decimal('14666.59'), Decimal('14682.94'), Decimal('14699.29'), Decimal('14715.64'), Decimal('14731.99'), Decimal('14748.34'), Decimal('14764.69'), Decimal('14781.04'), Decimal('14797.39'), Decimal('14813.74'), Decimal('14830.09'), Decimal(
            '14846.44'), Decimal('14862.79'), Decimal('14879.14'), Decimal('14895.49'), Decimal('14911.84'), Decimal('14928.19'), Decimal('14944.54'), Decimal('14960.89'), Decimal('14977.24'), Decimal('14993.59'), Decimal('15009.94'), Decimal('15026.29'), Decimal('15042.64'), Decimal('15058.99'), Decimal('15075.34'), Decimal('15091.69'), Decimal('15108.04'), Decimal('15124.39'), Decimal('15140.74'), Decimal('15157.09'), Decimal('15173.44'), Decimal('15189.79'), Decimal('15206.14'), Decimal('15222.49'), Decimal('15238.84'),
        Decimal('15255.19'), Decimal('15271.54'), Decimal('15287.89'), Decimal('15304.24'), Decimal('15320.59'), Decimal('15336.94'), Decimal('15353.29'), Decimal('15369.64'), Decimal('15385.99'), Decimal('15402.34'), Decimal('15418.69'), Decimal('15435.04'), Decimal('15451.39'), Decimal('15467.74'), Decimal('15484.09'), Decimal('15500.44'), Decimal('15516.79'), Decimal('15533.14'), Decimal('15549.49'), Decimal('15565.84'), Decimal('15582.19'), Decimal('15598.54'), Decimal('15614.89'), Decimal('15631.24'), Decimal(
            '15647.59'), Decimal('15663.94'), Decimal('15680.29'), Decimal('15696.64'), Decimal('15712.99'), Decimal('15729.34'), Decimal('15745.69'), Decimal('15762.04'), Decimal('15778.39'), Decimal('15794.74'), Decimal('15811.09'), Decimal('15827.44'), Decimal('15843.79'), Decimal('15860.14'), Decimal('15876.49'), Decimal('15892.84'), Decimal('15909.19'), Decimal('15925.54'), Decimal('15941.89'), Decimal('15958.24'), Decimal('15974.59'), Decimal('15990.94'), Decimal('16007.29'), Decimal('16023.64'), Decimal('16039.99'),
        Decimal('16056.34'), Decimal('16072.69'), Decimal('16089.04'), Decimal('16105.39'), Decimal('16121.74'), Decimal('16138.09'), Decimal('16154.44'), Decimal('16170.79'), Decimal('16187.14'), Decimal('16203.49'), Decimal('16219.84'), Decimal('16236.19'), Decimal('16252.54'), Decimal('16268.89'), Decimal('16285.24'), Decimal('16301.59'), Decimal('16317.94'), Decimal('16334.29'), Decimal('16350.64'), Decimal('16366.99'), Decimal('16383.34'), Decimal('16399.69'), Decimal('16416.04'), Decimal('16432.39'), Decimal(
            '16448.74'), Decimal('16465.09'), Decimal('16481.44'), Decimal('16497.79'), Decimal('16514.14'), Decimal('16530.49'), Decimal('16546.84'), Decimal('16563.19'), Decimal('16579.54'), Decimal('16595.89'), Decimal('16612.24'), Decimal('16628.59'), Decimal('16644.94'), Decimal('16661.29'), Decimal('16677.64'), Decimal('16693.99'), Decimal('16710.34'), Decimal('16726.69'), Decimal('16743.04'), Decimal('16759.39'), Decimal('16775.74'), Decimal('16792.09'), Decimal('16808.44'), Decimal('16824.79'), Decimal('16841.14'),
        Decimal('16857.49'), Decimal('16873.84'), Decimal('16890.19'), Decimal('16906.54'), Decimal('16922.89'), Decimal('16939.24'), Decimal('16955.59'), Decimal('16971.94'), Decimal('16988.29'), Decimal('17004.64'), Decimal('17020.99'), Decimal('17037.34'), Decimal('17053.69'), Decimal('17070.04'), Decimal('17086.39'), Decimal('17102.74'), Decimal('17119.09'), Decimal('17135.44'), Decimal('17151.79'), Decimal('17168.14'), Decimal('17184.49'), Decimal('17200.84'), Decimal('17217.19'), Decimal('17233.54'), Decimal(
            '17249.89'), Decimal('17266.24'), Decimal('17282.59'), Decimal('17298.94'), Decimal('17315.29'), Decimal('17331.64'), Decimal('17347.99'), Decimal('17364.34'), Decimal('17380.69'), Decimal('17397.04'), Decimal('17413.39'), Decimal('17429.74'), Decimal('17446.09'), Decimal('17462.44'), Decimal('17478.79'), Decimal('17495.14'), Decimal('17511.49'), Decimal('17527.84'), Decimal('17544.19'), Decimal('17560.54'), Decimal('17576.89'), Decimal('17593.24'), Decimal('17609.59'), Decimal('17625.94'), Decimal('17642.29'),
        Decimal('17658.64'), Decimal('17674.99'), Decimal('17691.34'), Decimal('17707.69'), Decimal('17724.04'), Decimal('17740.39'), Decimal('17756.74'), Decimal('17773.09'), Decimal('17789.44'), Decimal('17805.79'), Decimal('17822.14'), Decimal('17838.49'), Decimal('17854.84'), Decimal('17871.19'), Decimal('17887.54'), Decimal('17903.89'), Decimal('17920.24'), Decimal('17936.59'), Decimal('17952.94'), Decimal('17969.29'), Decimal('17985.64'), Decimal('18001.99'), Decimal('18018.34'), Decimal('18034.69'), Decimal(
            '18051.04'), Decimal('18067.39'), Decimal('18083.74'), Decimal('18100.09'), Decimal('18116.44'), Decimal('18132.79'), Decimal('18149.14'), Decimal('18165.49'), Decimal('18181.84'), Decimal('18198.19'), Decimal('18214.54'), Decimal('18230.89'), Decimal('18247.24'), Decimal('18263.59'), Decimal('18279.94'), Decimal('18296.29'), Decimal('18312.64'), Decimal('18328.99'), Decimal('18345.34'), Decimal('18361.69'), Decimal('18378.04'), Decimal('18394.39'), Decimal('18410.74'), Decimal('18427.09'), Decimal('18443.44'),
        Decimal('18459.79'), Decimal('18476.14'), Decimal('18492.49'), Decimal('18508.84'), Decimal('18525.19'), Decimal('18541.54'), Decimal('18557.89'), Decimal('18574.24'), Decimal('18590.59'), Decimal('18606.94'), Decimal('18623.29'), Decimal('18639.64'), Decimal('18655.99'), Decimal('18672.34'), Decimal('18688.69'), Decimal('18705.04'), Decimal('18721.39'), Decimal('18737.74'), Decimal('18754.09'), Decimal('18770.44'), Decimal('18786.79'), Decimal('18803.14'), Decimal('18819.49'), Decimal('18835.84'), Decimal(
            '18852.19'), Decimal('18868.54'), Decimal('18884.89'), Decimal('18901.24'), Decimal('18917.59'), Decimal('18933.94'), Decimal('18950.29'), Decimal('18966.64'), Decimal('18982.99'), Decimal('18999.34'), Decimal('19015.69'), Decimal('19032.04'), Decimal('19048.39'), Decimal('19064.74'), Decimal('19081.09'), Decimal('19097.44'), Decimal('19113.79'), Decimal('19130.14'), Decimal('19146.49'), Decimal('19162.84'), Decimal('19179.19'), Decimal('19195.54'), Decimal('19211.89'), Decimal('19228.24'), Decimal('19244.59'),
        Decimal('19260.94'), Decimal('19277.29'), Decimal('19293.64'), Decimal('19309.99'), Decimal('19326.34'), Decimal('19342.69'), Decimal('19359.04'), Decimal('19375.39'), Decimal('19391.74'), Decimal('19408.09'), Decimal('19424.44'), Decimal('19440.79'), Decimal('19457.14'), Decimal('19473.49'), Decimal('19489.84'), Decimal('19506.19'), Decimal('19522.54'), Decimal('19538.89'), Decimal('19555.24'), Decimal('19571.59'), Decimal('19587.94'), Decimal('19604.29'), Decimal('19620.64'), Decimal('19636.99'), Decimal(
            '19653.34'), Decimal('19669.69'), Decimal('19686.04'), Decimal('19702.39'), Decimal('19718.74'), Decimal('19735.09'), Decimal('19751.44'), Decimal('19767.79'), Decimal('19784.14'), Decimal('19800.49'), Decimal('19816.84'), Decimal('19833.19'), Decimal('19849.54'), Decimal('19865.89'), Decimal('19882.24'), Decimal('19898.59'), Decimal('19914.94'), Decimal('19931.29'), Decimal('19947.64'), Decimal('19963.99'), Decimal('19980.34'), Decimal('19996.69'), Decimal('20013.04'), Decimal('20029.39'), Decimal('20045.74'),
        Decimal('20062.09'), Decimal('20078.44'), Decimal('20094.79'), Decimal('20111.14'), Decimal('20127.49'), Decimal('20143.84'), Decimal('20160.19'), Decimal('20176.54'), Decimal('20192.89'), Decimal('20209.24'), Decimal('20225.59'), Decimal('20241.94'), Decimal('20258.29'), Decimal('20274.64'), Decimal('20290.99'), Decimal('20307.34'), Decimal('20323.69'), Decimal('20340.04'), Decimal('20356.39'), Decimal('20372.74'), Decimal('20389.09'), Decimal('20405.44'), Decimal('20421.79'), Decimal('20438.14'), Decimal(
            '20454.49'), Decimal('20470.84'), Decimal('20487.19'), Decimal('20503.54'), Decimal('20519.89'), Decimal('20536.24'), Decimal('20552.59'), Decimal('20568.94'), Decimal('20585.29'), Decimal('20601.64'), Decimal('20617.99'), Decimal('20634.34'), Decimal('20650.69'), Decimal('20667.04'), Decimal('20683.39'), Decimal('20699.74'), Decimal('20716.09'), Decimal('20732.44'), Decimal('20748.79'), Decimal('20765.14'), Decimal('20781.49'), Decimal('20797.84'), Decimal('20814.19'), Decimal('20830.54'), Decimal('20846.89'),
        Decimal('20863.24'), Decimal('20879.59'), Decimal('20895.94'), Decimal('20912.29'), Decimal('20928.64'), Decimal('20944.99'), Decimal('20961.34'), Decimal('20977.69'), Decimal('20994.04'), Decimal('21010.39'), Decimal('21026.74'), Decimal('21043.09'), Decimal('21059.44'), Decimal('21075.79'), Decimal('21092.14'), Decimal('21108.49'), Decimal('21124.84'), Decimal('21141.19'), Decimal('21157.54'), Decimal('21173.89'), Decimal('21190.24'), Decimal('21206.59'), Decimal('21222.94'), Decimal('21239.29'), Decimal(
            '21255.64'), Decimal('21271.99'), Decimal('21288.34'), Decimal('21304.69'), Decimal('21321.04'), Decimal('21337.39'), Decimal('21353.74'), Decimal('21370.09'), Decimal('21386.44'), Decimal('21402.79'), Decimal('21419.14'), Decimal('21435.49'), Decimal('21451.84'), Decimal('21468.19'), Decimal('21484.54'), Decimal('21500.89'), Decimal('21517.24'), Decimal('21533.59'), Decimal('21549.94'), Decimal('21566.29'), Decimal('21582.64'), Decimal('21598.99'), Decimal('21615.34'), Decimal('21631.69'), Decimal('21648.04'),
        Decimal('21664.39'), Decimal('21680.74'), Decimal('21697.09'), Decimal('21713.44'), Decimal('21729.79'), Decimal('21746.14'), Decimal('21762.49'), Decimal('21778.84'), Decimal('21795.19'), Decimal('21811.54'), Decimal('21827.89'), Decimal('21844.24'), Decimal('21860.59'), Decimal('21876.94'), Decimal('21893.29'), Decimal('21909.64'), Decimal('21925.99'), Decimal('21942.34'), Decimal('21958.69'), Decimal('21975.04'), Decimal('21991.39'), Decimal('22007.74'), Decimal('22024.09'), Decimal('22040.44'), Decimal(
            '22056.79'), Decimal('22073.14'), Decimal('22089.49'), Decimal('22105.84'), Decimal('22122.19'), Decimal('22138.54'), Decimal('22154.89'), Decimal('22171.24'), Decimal('22187.59'), Decimal('22203.94'), Decimal('22220.29'), Decimal('22236.64'), Decimal('22252.99'), Decimal('22269.34'), Decimal('22285.69'), Decimal('22302.04'), Decimal('22318.39'), Decimal('22334.74'), Decimal('22351.09'), Decimal('22367.44'), Decimal('22383.79'), Decimal('22400.14'), Decimal('22416.49'), Decimal('22432.84'), Decimal('22449.19'),
        Decimal('22465.54'), Decimal('22481.89'), Decimal('22498.24'), Decimal('22514.59'), Decimal('22530.94'), Decimal('22547.29'), Decimal('22563.64'), Decimal('22579.99'), Decimal('22596.34'), Decimal('22612.69'), Decimal('22629.04'), Decimal('22645.39'), Decimal('22661.74'), Decimal('22678.09'), Decimal('22694.44'), Decimal('22710.79'), Decimal('22727.14'), Decimal('22743.49'), Decimal('22759.84'), Decimal('22776.19'), Decimal('22792.54'), Decimal('22808.89'), Decimal('22825.24'), Decimal('22841.59'), Decimal(
            '22857.94'), Decimal('22874.29'), Decimal('22890.64'), Decimal('22906.99'), Decimal('22923.34'), Decimal('22939.69'), Decimal('22956.04'), Decimal('22972.39'), Decimal('22988.74'), Decimal('23005.09'), Decimal('23021.44'), Decimal('23037.79'), Decimal('23054.14'), Decimal('23070.49'), Decimal('23086.84'), Decimal('23103.19'), Decimal('23119.54'), Decimal('23135.89'), Decimal('23152.24'), Decimal('23168.59'), Decimal('23184.94'), Decimal('23201.29'), Decimal('23217.64'), Decimal('23233.99'), Decimal('23250.34'),
        Decimal('23266.69'), Decimal('23283.04'), Decimal('23299.39'), Decimal('23315.74'), Decimal('23332.09'), Decimal('23348.44'), Decimal('23364.79'), Decimal('23381.14'), Decimal('23397.49'), Decimal('23413.84'), Decimal('23430.19'), Decimal('23446.54'), Decimal('23462.89'), Decimal('23479.24'), Decimal('23495.59'), Decimal('23511.94'), Decimal('23528.29'), Decimal('23544.64'), Decimal('23560.99'), Decimal('23577.34'), Decimal('23593.69'), Decimal('23610.04'), Decimal('23626.39'), Decimal('23642.74'), Decimal(
            '23659.09'), Decimal('23675.44'), Decimal('23691.79'), Decimal('23708.14'), Decimal('23724.49'), Decimal('23740.84'), Decimal('23757.19'), Decimal('23773.54'), Decimal('23789.89'), Decimal('23806.24'), Decimal('23822.59'), Decimal('23838.94'), Decimal('23855.29'), Decimal('23871.64'), Decimal('23887.99'), Decimal('23904.34'), Decimal('23920.69'), Decimal('23937.04'), Decimal('23953.39'), Decimal('23969.74'), Decimal('23986.09'), Decimal('24002.44'), Decimal('24018.79'), Decimal('24035.14'), Decimal('24051.49'),
        Decimal('24067.84'), Decimal('24084.19'), Decimal('24100.54'), Decimal('24116.89'), Decimal('24133.24'), Decimal('24149.59'), Decimal('24165.94'), Decimal('24182.29'), Decimal('24198.64'), Decimal('24214.99'), Decimal('24231.34'), Decimal('24247.69'), Decimal('24264.04'), Decimal('24280.39'), Decimal('24296.74'), Decimal('24313.09'), Decimal('24329.44'), Decimal('24345.79'), Decimal('24362.14'), Decimal('24378.49'), Decimal('24394.84'), Decimal('24411.19'), Decimal('24427.54'), Decimal('24443.89'), Decimal(
            '24460.24'), Decimal('24476.59'), Decimal('24492.94'), Decimal('24509.29'), Decimal('24525.64'), Decimal('24541.99'), Decimal('24558.34'), Decimal('24574.69'), Decimal('24591.04'), Decimal('24607.39'), Decimal('24623.74'), Decimal('24640.09'), Decimal('24656.44'), Decimal('24672.79'), Decimal('24689.14'), Decimal('24705.49'), Decimal('24721.84'), Decimal('24738.19'), Decimal('24754.54'), Decimal('24770.89'), Decimal('24787.24'), Decimal('24803.59'), Decimal('24819.94'), Decimal('24836.29'), Decimal('24852.64'),
        Decimal('24868.99'), Decimal('24885.34'), Decimal('24901.69'), Decimal('24918.04'), Decimal('24934.39'), Decimal('24950.74'), Decimal('24967.09'), Decimal('24983.44'), Decimal('24999.79'), Decimal('25016.14'), Decimal('25032.49'), Decimal('25048.84'), Decimal('25065.19'), Decimal('25081.54'), Decimal('25097.89'), Decimal('25114.24'), Decimal('25130.59'), Decimal('25146.94'), Decimal('25163.29'), Decimal('25179.64'), Decimal('25195.99'), Decimal('25212.34'), Decimal('25228.69'), Decimal('25245.04'), Decimal(
            '25261.39'), Decimal('25277.74'), Decimal('25294.09'), Decimal('25310.44'), Decimal('25326.79'), Decimal('25343.14'), Decimal('25359.49'), Decimal('25375.84'), Decimal('25392.19'), Decimal('25408.54'), Decimal('25424.89'), Decimal('25441.24'), Decimal('25457.59'), Decimal('25473.94'), Decimal('25490.29'), Decimal('25506.64'), Decimal('25522.99'), Decimal('25539.34'), Decimal('25555.69'), Decimal('25572.04'), Decimal('25588.39'), Decimal('25604.74'), Decimal('25621.09'), Decimal('25637.44'), Decimal('25653.79'),
        Decimal('25670.14'), Decimal('25686.49'), Decimal('25702.84'), Decimal('25719.19'), Decimal('25735.54'), Decimal('25751.89'), Decimal('25768.24'), Decimal('25784.59'), Decimal('25800.94'), Decimal('25817.29'), Decimal('25833.64'), Decimal('25849.99'), Decimal('25866.34'), Decimal('25882.69'), Decimal('25899.04'), Decimal('25915.39'), Decimal('25931.74'), Decimal('25948.09'), Decimal('25964.44'), Decimal('25980.79'), Decimal('25997.14'), Decimal('26013.49'), Decimal('26029.84'), Decimal('26046.19'), Decimal(
            '26062.54'), Decimal('26078.89'), Decimal('26095.24'), Decimal('26111.59'), Decimal('26127.94'), Decimal('26144.29'), Decimal('26160.64'), Decimal('26176.99'), Decimal('26193.34'), Decimal('26209.69'), Decimal('26226.04'), Decimal('26242.39'), Decimal('26258.74'), Decimal('26275.09'), Decimal('26291.44'), Decimal('26307.79'), Decimal('26324.14'), Decimal('26340.49'), Decimal('26356.84'), Decimal('26373.19'), Decimal('26389.54'), Decimal('26405.89'), Decimal('26422.24'), Decimal('26438.59'), Decimal('26454.94'),
        Decimal('26471.29'), Decimal('26487.64'), Decimal('26503.99'), Decimal('26520.34'), Decimal('26536.69'), Decimal('26553.04'), Decimal('26569.39'), Decimal('26585.74'), Decimal('26602.09'), Decimal('26618.44'), Decimal('26634.79'), Decimal('26651.14'), Decimal('26667.49'), Decimal('26683.84'), Decimal('26700.19'), Decimal('26716.54'), Decimal('26732.89'), Decimal('26749.24'), Decimal('26765.59'), Decimal('26781.94'), Decimal('26798.29'), Decimal('26814.64'), Decimal('26830.99'), Decimal('26847.34'), Decimal(
            '26863.69'), Decimal('26880.04'), Decimal('26896.39'), Decimal('26912.74'), Decimal('26929.09'), Decimal('26945.44'), Decimal('26961.79'), Decimal('26978.14'), Decimal('26994.49'), Decimal('27010.84'), Decimal('27027.19'), Decimal('27043.54'), Decimal('27059.89'), Decimal('27076.24'), Decimal('27092.59'), Decimal('27108.94'), Decimal('27125.29'), Decimal('27141.64'), Decimal('27157.99'), Decimal('27174.34'), Decimal('27190.69'), Decimal('27207.04'), Decimal('27223.39'), Decimal('27239.74'), Decimal('27256.09'),
        Decimal('27272.44'), Decimal('27288.79'), Decimal('27305.14'), Decimal('27321.49'), Decimal('27337.84'), Decimal('27354.19'), Decimal('27370.54'), Decimal('27386.89'), Decimal('27403.24'), Decimal('27419.59'), Decimal('27435.94'), Decimal('27452.29'), Decimal('27468.64'), Decimal('27484.99'), Decimal('27501.34'), Decimal('27517.69'), Decimal('27534.04'), Decimal('27550.39'), Decimal('27566.74'), Decimal('27583.09'), Decimal('27599.44'), Decimal('27615.79'), Decimal('27632.14'), Decimal('27648.49'), Decimal(
            '27664.84'), Decimal('27681.19'), Decimal('27697.54'), Decimal('27713.89'), Decimal('27730.24'), Decimal('27746.59'), Decimal('27762.94'), Decimal('27779.29'), Decimal('27795.64'), Decimal('27811.99'), Decimal('27828.34'), Decimal('27844.69'), Decimal('27861.04'), Decimal('27877.39'), Decimal('27893.74'), Decimal('27910.09'), Decimal('27926.44'), Decimal('27942.79'), Decimal('27959.14'), Decimal('27975.49'), Decimal('27991.84'), Decimal('28008.19'), Decimal('28024.54'), Decimal('28040.89'), Decimal('28057.24'),
        Decimal('28073.59'), Decimal('28089.94'), Decimal('28106.29'), Decimal('28122.64'), Decimal('28138.99'), Decimal('28155.34'), Decimal('28171.69'), Decimal('28188.04'), Decimal('28204.39'), Decimal('28220.74'), Decimal('28237.09'), Decimal('28253.44'), Decimal('28269.79'), Decimal('28286.14'), Decimal('28302.49'), Decimal('28318.84'), Decimal('28335.19'), Decimal('28351.54'), Decimal('28367.89'), Decimal('28384.24'), Decimal('28400.59'), Decimal('28416.94'), Decimal('28433.29'), Decimal('28449.64'), Decimal(
            '28465.99'), Decimal('28482.34'), Decimal('28498.69'), Decimal('28515.04'), Decimal('28531.39'), Decimal('28547.74'), Decimal('28564.09'), Decimal('28580.44'), Decimal('28596.79'), Decimal('28613.14'), Decimal('28629.49'), Decimal('28645.84'), Decimal('28662.19'), Decimal('28678.54'), Decimal('28694.89'), Decimal('28711.24'), Decimal('28727.59'), Decimal('28743.94'), Decimal('28760.29'), Decimal('28776.64'), Decimal('28792.99'), Decimal('28809.34'), Decimal('28825.69'), Decimal('28842.04'), Decimal('28858.39'),
        Decimal('28874.74'), Decimal('28891.09'), Decimal('28907.44'), Decimal('28923.79'), Decimal('28940.14'), Decimal('28956.49'), Decimal('28972.84'), Decimal('28989.19'), Decimal('29005.54'), Decimal('29021.89'), Decimal('29038.24'), Decimal('29054.59'), Decimal('29070.94'), Decimal('29087.29'), Decimal('29103.64'), Decimal('29119.99'), Decimal('29136.34'), Decimal('29152.69'), Decimal('29169.04'), Decimal('29185.39'), Decimal('29201.74'), Decimal('29218.09'), Decimal('29234.44'), Decimal('29250.79'), Decimal(
            '29267.14'), Decimal('29283.49'), Decimal('29299.84'), Decimal('29316.19'), Decimal('29332.54'), Decimal('29348.89'), Decimal('29365.24'), Decimal('29381.59'), Decimal('29397.94'), Decimal('29414.29'), Decimal('29430.64'), Decimal('29446.99'), Decimal('29463.34'), Decimal('29479.69'), Decimal('29496.04'), Decimal('29512.39'), Decimal('29528.74'), Decimal('29545.09'), Decimal('29561.44'), Decimal('29577.79'), Decimal('29594.14'), Decimal('29610.49'), Decimal('29626.84'), Decimal('29643.19'), Decimal('29659.54'),
        Decimal('29675.89'), Decimal('29692.24'), Decimal('29708.59'), Decimal('29724.94'), Decimal('29741.29'), Decimal('29757.64'), Decimal('29773.99'), Decimal('29790.34'), Decimal('29806.69'), Decimal('29823.04'), Decimal('29839.39'), Decimal('29855.74'), Decimal('29872.09'), Decimal('29888.44'), Decimal('29904.79'), Decimal('29921.14'), Decimal('29937.49'), Decimal('29953.84'), Decimal('29970.19'), Decimal('29986.54'), Decimal('30002.89'), Decimal('30019.24'), Decimal('30035.59'), Decimal('30051.94'), Decimal(
            '30068.29'), Decimal('30084.64'), Decimal('30100.99'), Decimal('30117.34'), Decimal('30133.69'), Decimal('30150.04'), Decimal('30166.39'), Decimal('30182.74'), Decimal('30199.09'), Decimal('30215.44'), Decimal('30231.79'), Decimal('30248.14'), Decimal('30264.49'), Decimal('30280.84'), Decimal('30297.19'), Decimal('30313.54'), Decimal('30329.89'), Decimal('30346.24'), Decimal('30362.59'), Decimal('30378.94'), Decimal('30395.29'), Decimal('30411.64'), Decimal('30427.99'), Decimal('30444.34'), Decimal('30460.69'),
        Decimal('30477.04'), Decimal('30493.39'), Decimal('30509.74'), Decimal('30526.09'), Decimal('30542.44'), Decimal('30558.79'), Decimal('30575.14'), Decimal('30591.49'), Decimal('30607.84'), Decimal('30624.19'), Decimal('30640.54'), Decimal('30656.89'), Decimal('30673.24'), Decimal('30689.59'), Decimal('30705.94'), Decimal('30722.29'), Decimal('30738.64'), Decimal('30754.99'), Decimal('30771.34'), Decimal('30787.69'), Decimal('30804.04'), Decimal('30820.39'), Decimal('30836.74'), Decimal('30853.09'), Decimal(
            '30869.44'), Decimal('30885.79'), Decimal('30902.14'), Decimal('30918.49'), Decimal('30934.84'), Decimal('30951.19'), Decimal('30967.54'), Decimal('30983.89'), Decimal('31000.24'), Decimal('31016.59'), Decimal('31032.94'), Decimal('31049.29'), Decimal('31065.64'), Decimal('31081.99'), Decimal('31098.34'), Decimal('31114.69'), Decimal('31131.04'), Decimal('31147.39'), Decimal('31163.74'), Decimal('31180.09'), Decimal('31196.44'), Decimal('31212.79'), Decimal('31229.14'), Decimal('31245.49'), Decimal('31261.84'),
        Decimal('31278.19'), Decimal('31294.54'), Decimal('31310.89'), Decimal('31327.24'), Decimal('31343.59'), Decimal('31359.94'), Decimal('31376.29'), Decimal('31392.64'), Decimal('31408.99'), Decimal('31425.34'), Decimal(
            '31441.69'), Decimal('31458.04'), Decimal('31474.39'), Decimal('31490.74'), Decimal('31507.09'), Decimal('31523.44'), Decimal('31539.79'), Decimal('31556.14'), Decimal('31572.49'), Decimal('31588.84'), Decimal('31605.19')
    ]
    note = Note('C', 0)
    harmonics = note.get_harmonics()
    assert len(harmonics) == len(want_harmonics)
    for i, harmonic in enumerate(harmonics):
        assert type(harmonic) == Decimal
        assert harmonic == want_harmonics[i]

    # Test the harmonics for the highest note.
    want_harmonics = []
    note = Note('B', 10)
    harmonics = note.get_harmonics()
    assert len(harmonics) == len(want_harmonics)


# Test the "get_octaves" method for Note objects.
def test_Note_get_octaves():
    # Test that we can calculate the octaves correctly for each of the
    # notes/octaves in our frequency table.
    for want_note, freqs in FREQ_TABLE.items():
        for i in range(len(freqs)):
            note = Note(want_note, i)
            octaves = note.get_octaves()
            assert len(octaves) == 10 - i
            for j, octave in enumerate(octaves):
                want_octave = i + j + 1
                want_freq = freqs[want_octave]
                assert octave.note == want_note
                assert octave.octave == want_octave
                assert octave.freq == want_freq
                assert str(octave.freq) == str(want_freq)
                assert str(octave) == f'{want_note}{want_octave}'


# Test the function "parse_note".
def test_parse_note():
    # Test no value.
    with pytest.raises(ValueError):
        parse_note('')

    # Test a short note.
    with pytest.raises(ValueError):
        parse_note('C')

    # Test a long note.
    with pytest.raises(ValueError):
        parse_note('C♯100')

    # Test an invalid note.
    with pytest.raises(ValueError):
        parse_note('Dc5')

    # Test an invalid octave.
    with pytest.raises(ValueError):
        parse_note('C11')

    # Test a negative octave.
    with pytest.raises(ValueError):
        parse_note('C-1')

    # Test expected note values.
    for want_note in NOTES:
        for want_octave in range(0, 11):
            s = f'{want_note}{want_octave}'
            note = parse_note(s)
            assert str(note) == s
            assert note.note == want_note
            assert note.octave == want_octave

    # Test valid flat symbols.
    note = parse_note(f'D{FLAT_SYMBOL}5')
    assert str(note) == f'C{SHARP_SYMBOL}5'
    note = parse_note(f'E{FLAT_SYMBOL}5')
    assert str(note) == f'D{SHARP_SYMBOL}5'
    note = parse_note(f'G{FLAT_SYMBOL}5')
    assert str(note) == f'F{SHARP_SYMBOL}5'
    note = parse_note(f'A{FLAT_SYMBOL}5')
    assert str(note) == f'G{SHARP_SYMBOL}5'
    note = parse_note(f'B{FLAT_SYMBOL}5')
    assert str(note) == f'A{SHARP_SYMBOL}5'

    # Test alternative flat symbols.
    note = parse_note(f'Db5')
    assert str(note) == f'C{SHARP_SYMBOL}5'
    note = parse_note(f'Eb5')
    assert str(note) == f'D{SHARP_SYMBOL}5'
    note = parse_note(f'Gb5')
    assert str(note) == f'F{SHARP_SYMBOL}5'
    note = parse_note(f'Ab5')
    assert str(note) == f'G{SHARP_SYMBOL}5'
    note = parse_note(f'Bb5')
    assert str(note) == f'A{SHARP_SYMBOL}5'

    # Test invalid flat symbols.
    with pytest.raises(KeyError):
        parse_note(f'C{FLAT_SYMBOL}5')
    with pytest.raises(KeyError):
        parse_note(f'Cb5')
    with pytest.raises(KeyError):
        parse_note(f'F{FLAT_SYMBOL}5')
    with pytest.raises(KeyError):
        parse_note(f'Fb5')

    # Test natural symbols.
    note = parse_note(f'C{NATURAL_SYMBOL}5')
    assert str(note) == 'C5'
    note = parse_note(f'D{NATURAL_SYMBOL}5')
    assert str(note) == 'D5'
    note = parse_note(f'E{NATURAL_SYMBOL}5')
    assert str(note) == 'E5'
    note = parse_note(f'F{NATURAL_SYMBOL}5')
    assert str(note) == 'F5'
    note = parse_note(f'G{NATURAL_SYMBOL}5')
    assert str(note) == 'G5'
    note = parse_note(f'A{NATURAL_SYMBOL}5')
    assert str(note) == 'A5'
    note = parse_note(f'B{NATURAL_SYMBOL}5')
    assert str(note) == 'B5'


# Test the function "freq_to_note".
def test_freq_to_note():
    # Test invalid frequencies.
    with pytest.raises(ValueError):
        freq_to_note(LOWEST_NOTE_FREQ - Decimal('.01'))
    with pytest.raises(ValueError):
        freq_to_note(HIGHEST_NOTE_FREQ + Decimal('.01'))

    # Test that we can nudge a note off the standard frequency and then find the
    # note closest to it.
    for want_note, want_freqs in FREQ_TABLE.items():
        for want_octave, want_freq in enumerate(want_freqs):
            perc = Decimal(str(want_freq * 2 / 100))
            if want_octave < 10 and want_octave % 2 == 0:
                test_freq = want_freq + perc
            else:
                test_freq = want_freq - perc

            note = freq_to_note(test_freq)
            assert note.note == want_note
            assert note.octave == want_octave
            assert note.freq == want_freq
            assert str(note.freq) == str(want_freq)
            assert str(note) == f'{want_note}{want_octave}'
