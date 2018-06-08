import argparse
import logging
import json
import sys

from bs4 import BeautifulSoup

from rsscrawler.extractor import Extractor


logger = logging.getLogger(__name__)


def parse_description(description):
    """
     Returns a dictionary with serialized description content(images, links and not empty paragraphs)
     :param description: The description html text
    :rtype: dict
    """
    description_contents = []
    soup = BeautifulSoup(description, "html.parser")

    if not soup:
        return description_contents

    for el in soup:
        d = Extractor(el).as_dict()
        if not d:
            continue

        description_contents.append(d)

    return description_contents


def parse_item(item):
    """
    Return a item dict with a formated title, link and description
    :param item: A beautifulsoup element with name 'item'
    :return:
    """
    rules = {
        'title': str,
        'link': str,
        'description': parsed_description
    }
    new_item = {}

    for tag, parser in rules.items():
        element = item.find(tag)
        if not element:
            continue

        new_item[tag] = parser(element.text)

    return new_item


def parse_feed(text):
    """Parse a xml and format into a dict of feeds
    :param text: a xml data text
    :rtype: dict
    """
    items = []
    xml = BeautifulSoup(text, "xml")

    for item in xml.find_all('item'):
        new_item = parse_item(item)
        if not new_item:
            continue

        items.append(new_item)

    return {'feed': items}


def arguments(args=None):
    parser = argparse.ArgumentParser(description='Export rss feed as json.')
    parser.add_argument('url', help='Feed url.')
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

    content = retrieve_feed(options.url)
    if not content:
        logger.error("No feed content!")
        return

    d = parse_feed(content)
    feed_json = json.dumps(d, ensure_ascii=False)

    return feed_json


if __name__ == '__main__':
    print(main())
