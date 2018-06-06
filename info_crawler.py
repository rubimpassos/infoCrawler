import logging
import json
import sys

import requests

from bs4 import BeautifulSoup
from requests import Timeout, ConnectionError, TooManyRedirects, RequestException


logger = logging.getLogger(__name__)


def request_url_data(url, *args, **kwargs):
    try:
        request = requests.get(url, *args, **kwargs)
        request.raise_for_status()
        if request.status_code == 200:
            return request.content
    except (Timeout, ConnectionError, TooManyRedirects, RequestException) as ex:
        logger.exception(ex)

    return None


def soup_this(data, *args, **kwargs):
    try:
        soup = BeautifulSoup(data, *args, **kwargs)
        return soup
    except Exception as e:
        logger.exception(e)

    return None


def get_content_obj(element, _type, process):
    obj = {}
    content = process(element)

    if content:
        obj['type'] = _type
        obj['content'] = content

    return obj


def process_image_content(element):
    return element['src']


def process_text_content(element):
    text = element.text or ""
    return element.text.strip()


def process_links_content(element):
    links = []
    for link in element.find_all('a'):
        links.append(link.get('href'))

    return links


def parsed_description(description):
    """Returns images, links and paragraphs of the description
    :rtype: dict
    """
    description_contents = []
    soup = soup_this(description, "html.parser")

    if soup:
        for el in soup:
            el_content = {}

            if el.name == 'div' and el.img:
                el_content = get_content_obj(el.img, "image", process_image_content)
            elif el.name == 'div' and el.ul:
                el_content = get_content_obj(el.ul, "links", process_links_content)
            elif el.name == 'p':
                el_content = get_content_obj(el, "text", process_text_content)

            if el_content:
                description_contents.append(el_content)

    return description_contents


def get_feed_items(items_soup):
    feed_items = []
    fields_rules = {
        'title': str,
        'link': str,
        'description': parsed_description
    }

    for item in items_soup:
        el = {}
        for field in fields_rules.keys():
            if item.find(field):
                el[field] = fields_rules[field](item.find(field).text)

        feed_items.append(el)

    return feed_items


def parse_feed(text):
    """Parse xml text and format into a dict of feeds
    :param text: a xml data text
    :rtype: dict
    """

    feed = {'feed': []}
    xml = soup_this(text, "xml")
    if xml:
        items = get_feed_items(xml.find_all('item'))
        feed['feed'] = items

    return feed


def main(arg):
    data = request_url_data("https://revistaautoesporte.globo.com/rss/ultimas/feed.xml")

    if data:
        feed = parse_feed(data)
        feed_json = json.dumps(feed, ensure_ascii=False)
        print(feed_json)


if __name__ == '__main__':
    main(sys.argv[1:])
