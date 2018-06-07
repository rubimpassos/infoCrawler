import json
import logging

from infocrawler.infocrawler import retrieve_feed, parse_feed
from infocrawler.cli import arguments, verbosity


logger = logging.getLogger(__name__)


def main():
    options = arguments()
    verbosity(options.verbose)

    content = retrieve_feed(options.url)
    if not content:
        logger.error("No feed content!")
        return -1

    d = parse_feed(content)
    feed_json = json.dumps(d, ensure_ascii=False)
    print(feed_json)

    return 0
