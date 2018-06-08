import json
import logging

from rsscrawler.cli import arguments, verbosity
from rsscrawler.crawler import parse_feed
from rsscrawler.retrivefeed import retrieve_feed


logger = logging.getLogger(__name__)


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
