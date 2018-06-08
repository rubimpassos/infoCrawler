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
