from scipy.io import wavfile
import numpy as np
import scipy.signal
from frequency import *
from note import *
from log import *


class Spectrum():
    def __init__(self, path):
        """ Initialize a new spectral analysis from a WAV file. """

        log(f'\nOpening WAV file at "{path}"')
        sample_rate, wav_data = wavfile.read(path)

        # Convert stereo mixes down into a single mono track.
        if len(wav_data.shape) > 1 and wav_data.shape[1] > 1:
            log("\tConverting from stereo to mono")
            wav_data = np.mean(wav_data, axis=1)

        # Calculate some info from the source.
        num_samples = wav_data.shape[0]
        freq_step = Decimal(sample_rate) / Decimal(num_samples)
        log(f"\tSample rate: {sample_rate}")
        log(f"\tNumber of samples: {num_samples}")
        log(f"\tTotal track length: {num_samples / sample_rate}s")
        log(f"\tFrequency step: {freq_step}Hz / sample")

        # Create the power spectrum by computing the Fourier Transform on the signal.
        log("Analyzing signal spectrum")
        fft_data = np.fft.fft(wav_data)

        log("\tLowest frequency: 0Hz")
        log(f"\tHighest frequency: {float(len(fft_data)) * sample_rate / num_samples}Hz")

        # We now have a list of frequencies and their data. We can ignore all
        # frequencies above the Nyquist limit (half the sample rate), because
        # they cannot be reliably reproduced from the digital signal.
        fft_data = fft_data[:num_samples // 2]

        # Convert the complex numbers representing wave phases into real numbers
        # representing the magnitude of each frequency.
        magnitudes = [0.0] * len(fft_data)
        for i in range(len(fft_data)):
            # Get the complex number at this position in the power spectrum.
            cmplx = fft_data[i]

            # The real part represents the amplitude of the cosine component.
            cosAmp = cmplx.real
            # The imaginary part represents the amplitude of the sine component.
            sinAmp = cmplx.imag

            # Get the magnitude by calculating the length of the hypotenuse of
            # the sinusoid in this phase.
            mag = np.sqrt(cosAmp**2 + sinAmp**2)

            # Double the magnitude to account for both sides of the signal and
            # shrink it by the number of samples in the audio file.
            magnitudes[i] = 2 * mag / num_samples

        self.path = path
        self.fft_data = fft_data
        self.magnitudes = magnitudes
        self.sample_rate = sample_rate
        self.freq_step = freq_step

    def get_frequency_at(self, index):
        """ Get the frequency at the given index in the power spectrum data. """

        if index < 0 or index >= len(self.fft_data):
            raise ValueError("Invalid index")

        # The number of items in the power spectrum (FFT data) is equal to the
        # number of samples in the audio file. Whereas an index in the audio
        # file represents the audio signal for that sample, an index in the
        # power spectrum represents a particular frequency. The range of
        # frequencies in the spectrum starts at 0 and goes up to the sample
        # rate. The first index in the spectrum represents a frequency of 0, and
        # the last index represents the frequency of the sample rate. To
        # determine which frequency corresponds to this particular index, we
        # only need to determine its position in the entire set of data (FFT
        # data) and find the corresponding frequency in the entire range of
        # frequencies (sample rate).
        return float(index) * self.sample_rate / (2*len(self.fft_data))

    def get_magnitude_at(self, index):
        """ Get the magnitude of the frequency at the given index in the
        power spectrum data. """

        if index < 0 or index >= len(self.magnitudes):
            raise ValueError("Invalid index")

        return self.magnitudes[index]

    def get_fund_freq(self, min_freq=150):
        """ Find the fundamental frequency for this audio sample. """

        if hasattr(self, 'fund_freq'):
            return self.fund_freq

        log("Determining fundamental frequency")
        log(f"\tUsing minimum frequency distance of {min_freq}Hz")

        # Calculate the minimum number of units in the power spectrum data that
        # each peak must have between it and the peak closest to it. The default
        # is 150Hz. This was chosen because we use harmonics to find the
        # fundamental frequency, and harmonics are separated by the Hz of the
        # fundamental frequency. It's uncommon to have a fundamental frequency
        # below 150Hz, so we can safely assume that peaks will be at least that
        # far away from each other. If we use a smaller number, then find_peaks
        # sometimes thinks that one peak is actually multiple peaks when the
        # main peak is wide and has jagged edges.
        min_peak_distance = min_freq / float(self.freq_step)

        # The prominence of each peak is the difference between the magnitude of
        # its strongest frequency and the magnitude of the frequency at the
        # base. We're using a value equal to 5% of the largest peak as the
        # minimum prominence that a peak should have, which should be a large
        # enough value that we shouldn't have too many peaks from edge
        # perturbations but a small enough value that we capture higher
        # harmonics.
        min_mag = min(self.magnitudes)
        max_mag = max(self.magnitudes)
        prominence = (max_mag - min_mag) * 5 / 100

        # Find the indices of the most prominent peaks in the spectrum. They
        # will ordered by frequency in ascending order.
        peaks = scipy.signal.find_peaks(self.magnitudes, distance=min_peak_distance, prominence=prominence)[0]

        # Get the frequency at each peak.
        peak_freqs = [self.get_frequency_at(index) for index in peaks]

        # Determine the fundamental frequency of the spectrum by figuring out
        # which frequency has the most harmonics.
        cnt = 0
        fund_freq = 0.0
        for i, freq in enumerate(peak_freqs):

            harm_cnt = 0
            for j in range(i+1, len(peak_freqs)):

                # Calculate the modulo of this frequency against the base
                # frequency, and see how far away it is form a harmonic.
                mod = peak_freqs[j] % freq
                if mod > freq / 2:
                    mod = freq - mod

                # If the frequency's modulp is within 3% of the base frequency,
                # then we'll assume it's a harmonic.
                perc = mod * 100.0 // freq
                if perc < 3:
                    harm_cnt += 1

            # If this frequency has more harmonics than any frequency so far,
            # we'll store is as the fundamental frequency for now.
            if harm_cnt > cnt:
                cnt = harm_cnt
                fund_freq = freq

        log(f"\tFundamental frequency: {fund_freq}Hz")
        self.fund_freq = fund_freq

        return fund_freq

    def get_harm_ratios(self, min_freq=150):
        """ Get the ratios of the harmonic frequencies as compared to the
        fundamental frequency for this audio sample. The resulting array
        contains the magnitude of each harmonic divided by the magnitude of the
        fundamental frequency, sorted in ascending order of frequency. """

        fund_freq = Decimal(self.get_fund_freq(min_freq))

        # The width of the window for each harmonic's peak will be 10% of the
        # distance between each harmonic.
        peak_width = (fund_freq / self.freq_step) // 10

        # Find the magnitude of every harmonic for this fundamental frequency,
        # up to the highest frequency in this spectrum.
        magnitudes = []

        freq = Decimal(fund_freq * 2)
        max_freq = Decimal(self.get_frequency_at(len(self.fft_data)-1))
        while freq < max_freq:

            # Calculate the start and end of the window around this harmonic in
            # which we'll look for a peak magnitude.
            center = freq // self.freq_step
            start = int(center - (peak_width//2))
            if start < 0:
                start = 0
            end = int(center + (peak_width//2))
            if end > len(self.magnitudes)-1:
                end = len(self.magnitudes)-1

            # Find the peak magnitude in this window and add it to the list.
            mag = max(self.magnitudes[start:end])
            magnitudes.append(Decimal(mag))

            freq += fund_freq

        # Calculate the ratio of every harmonic's magnitude to the magnitude of
        # the fundamental frequency.
        fund_freq_index = fund_freq // self.freq_step
        fund_freq_mag = self.get_magnitude_at(int(fund_freq_index))
        ratios = [float(mag / Decimal(fund_freq_mag)) for mag in magnitudes]

        return ratios
