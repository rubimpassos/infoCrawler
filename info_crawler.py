import argparse
import logging
import json
import sys

import requests

from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


def retrieve_feed(url, **kwargs):
    content = ""

    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=3)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        response = session.get(url, **kwargs)
        response.raise_for_status()
        content = response.content
    except Exception as ex:
        logger.exception(ex)

    return content


def extract_image_url(element):
    return element['src']


def extract_text_content(element):
    text = element.text or ""
    return text.strip()


def extract_links(element):
    links = []
    for link in element.find_all('a'):
        links.append(link.get('href'))

    return links


def parsed_description(description):
    """Returns images, links and paragraphs of the description
    :rtype: dict
    """
    description_contents = []
    soup = BeautifulSoup(description, "html.parser")

    if not soup:
        return description_contents

    for el in soup:
        extracted_content, content_type = "", ""
        if el.name == 'div' and el.img:
            extracted_content = extract_image_url(el.img)
            content_type = "image"
        elif el.name == 'div' and el.ul:
            extracted_content = extract_links(el.ul)
            content_type = "links"
        elif el.name == 'p':
            extracted_content = extract_text_content(el)
            content_type = "text"

        if not extracted_content:
            continue

        description_contents.append({
            'type': content_type,
            'content': extracted_content
        })

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
