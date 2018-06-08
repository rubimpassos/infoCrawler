import logging
import sys
from argparse import ArgumentParser
from pathlib import Path

from infocrawler.crawler import feed_reader


logger = logging.getLogger(__name__)


def arguments(args=None):
    parser = ArgumentParser(description='Export rss feed as json.')
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


def main():
    options = arguments()
    verbosity(options.verbose)

    if options.file and options.file.exists():
        sys.exit("File already exists!")

    json_string = feed_reader(options.url)
    if not options.file:
        print(json_string)
        return 0

    options.file.write_text(json_string, encoding='utf-8')
    return 0
