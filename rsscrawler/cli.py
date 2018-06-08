import argparse
import logging

import sys
from pathlib import Path


def arguments(args=None):
    parser = argparse.ArgumentParser(description='Export rss feed as json.')
    parser.add_argument('url', help='Feed url.')
    parser.add_argument('-f', '--file', help='Save output in file path.', type=Path, default=None)
    parser.add_argument('-v', '--verbose', type=int, choices=[1, 2], default=1)

    return parser.parse_args(args)


def verbosity(level):
    if level < 2:
        return

    root = logging.getLogger()
    console = logging.StreamHandler(sys.stdout)
    root.addHandler(console)
    root.setLevel(logging.DEBUG)
