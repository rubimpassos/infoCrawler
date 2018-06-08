import json
import logging

from bs4 import BeautifulSoup

from infocrawler.extractor import Extractor
from infocrawler.retrivefeed import retrieve_feed

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
        type_, content = Extractor(el).extract()

        if not type_ or not content:
            continue

        description_contents.append({
            'type': type_,
            'content': content
        })

    return description_contents


def parse_item(item):
    """
    Returns a dictionary with seralized item of the feed, with formatted title, link and description
    :param item: A BeautifulSoup element with name 'item'
    """
    rules = {
        'title': str,
        'link': str,
        'description': parse_description
    }
    new_item = {}

    for tag, parser in rules.items():
        element = item.find(tag)
        if not element:
            continue

        new_item[tag] = parser(element.text)

    return new_item


def feed_parser(text):
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


def feed_reader(url):
    """Returns json from feed url"""
    content = retrieve_feed(url)
    d = feed_parser(content)
    json_string = json.dumps(d, ensure_ascii=False)

    return json_string
