#!/usr/bin/env python3
import argparse
from eca import eca
import logging

def parse_arguments():
    parser = argparse.ArgumentParser()

    regex_default = r'^(.*)$'
    regex_desc = f"Regular expression for selecting time and possible time range, defaults to {regex_default}"
    parser.add_argument("--regex1", default=regex_default, help=regex_desc)
    parser.add_argument("--regex2", default=regex_default, help=regex_desc)

    format_default = "iso"
    format_desc = f"Format for parsing times from first file, default {format_default}. Either 'iso' or see pydoc time.strptime."
    parser.add_argument("--time-format1", default=format_default, help=format_desc)
    parser.add_argument("--time-format2", default=format_default, help=format_desc)

    parser.add_argument("--time-margin", default="10", help="number of seconds for time stamp to be considered coincident")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-o", "--overlap", default=1.0, type=float, help="How much overlaping time (in seconds) to work with.")

    parser.add_argument("files", nargs=2, help="input files")

    return parser.parse_args()
def main():
    args = parse_arguments()
    if args.verbose:
        eca.logger.setLevel(logging.INFO)

    parsers = list()

    for i in range(2):
        format = getattr(args, f"time_format{i+1}")
        p = eca.ParserFactory.get_parser(format)
        p.set_overlap(args.overlap)
        parsers.append(p)

    (coincidents, misses) = eca.compare_files(args.files, parsers)
    print(f"{coincidents} coincidents and {misses} misses")


if __name__ == "__main__":
    main()
