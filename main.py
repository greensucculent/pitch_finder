import argparse
import os.path
from spectrum import *

if __name__ == '__main__':

    # Parse the command-line arguments.
    parser = argparse.ArgumentParser(description="Analyze a tone from a WAV file.")
    parser.add_argument('path', type=str, nargs='+', help="Paths to files to analyze")
    parser.add_argument('--min', dest='min_freq', type=int, default=150,
                        help="Minimum fundamental frequency")
    parser.add_argument('-v', dest='logging_enabled', action='store_true',
                        help="Enable verbose logging")
    args = parser.parse_args()

    set_logging(args.logging_enabled)

    for path in args.path:
        if not os.path.exists(path):
            raise FileExistsError(f'"{path}" is not a readable file')

        spectrum = Spectrum(path)
        print(path, spectrum.get_fund_freq(), spectrum.get_harm_ratios())
