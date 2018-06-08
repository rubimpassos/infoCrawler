import argparse
import json
import logging
import sys
from pathlib import Path

from rsscrawler.crawler import parse_feed
from rsscrawler.retrivefeed import retrieve_feed


logger = logging.getLogger(__name__)


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


def main():
    options = arguments()
    verbosity(options.verbose)

    logger.info("Requesting feed...")
    content = retrieve_feed(options.url)
    if not content:
        logger.error("No feed content!")
        return -1

    logger.info("Parsing feed content...")
    d = parse_feed(content)

    logger.info("Dumping into json format...")
    json_string = json.dumps(d, ensure_ascii=False)

    if not options.file:
        print(json_string)
        return 0

    f = options.file.resolve()
    if f.exists():
        logger.error("File already exists!")
        return -1

    f.write_text(json_string, encoding='utf-8')

    return 0
