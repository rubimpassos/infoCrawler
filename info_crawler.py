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


def parse_soup(data, *args, **kwargs):
    try:
        soup = BeautifulSoup(data, *args, **kwargs)
        return soup
    except Exception as e:
        logger.exception(e)

    return None


def parsed_description(description):
    """Returns images, links and paragraphs of the description
    :rtype: dict
    """
    soup = parse_soup(description, "html.parser")
    content = []

    if soup:
        for el in soup:
            if el.name == 'div':
                if el.img:
                    content.append({
                        'type': "image",
                        'content': el.img['src']
                    })
                # check if div<ul<li<a exists
                elif el.ul and el.ul.li and el.ul.li.a:
                    links = []
                    for link in el.ul:
                        a_tag = link.find('a')
                        if a_tag != -1 and a_tag.get('href'):
                            links.append(a_tag.get('href'))

                    if len(links) > 0:
                        content.append({
                            'type': "links",
                            'content': links
                        })
            elif el.name == 'p' and el.text and el.text.strip():
                content.append({
                    'type': "text",
                    'content': el.text.strip()
                })
    return content


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
                el[field] = fields_rules[field](item.find('title').text)

        feed_items.append(el)

    return feed_items


def parse_feed(text):
    """Parse xml text and format into a dict of feeds
    :param text: a xml data text
    :rtype: dict
    """

    feed = {'feed': []}
    xml = parse_soup(text, "xml")
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
