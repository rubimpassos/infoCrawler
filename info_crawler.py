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


def mount_description_content(_type, content):
    obj = {}

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
    soup = BeautifulSoup(description, "html.parser")

    if soup:
        for el in soup:
            el_content = {}

            if el.name == 'div' and el.img:
                content = process_image_content(el.img)
                el_content = mount_description_content("image", content)
            elif el.name == 'div' and el.ul:
                content = process_links_content(el.ul)
                el_content = mount_description_content("links", content)
            elif el.name == 'p':
                content = process_text_content(el)
                el_content = mount_description_content("text", content)

            if el_content:
                description_contents.append(el_content)

    return description_contents


def parse_item(item):
    """
    Return a item dict with a formated title, link and description
    :param item: A beautifulsoup element with name 'item'
    :return:
    """
    new_item = {}

    title = item.find('title')
    if title:
        new_item[title.name] = title.text

    link = item.find('link')
    if link:
        new_item[link.name] = link.text

    description = item.find('description')
    if description:
        new_item[description.name] = parsed_description(description.text)

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

        if new_item:
            items.append(new_item)

        items.append(new_item)

    return {'feed': items}


def main(args):
    content = retrieve_feed("https://revistaautoesporte.globo.com/rss/ultimas/f.xml")

    if not content:
        logger.error("No feed content found!")
        return -1

    d = parse_feed(content)
    feed_json = json.dumps(d, ensure_ascii=False)

    return feed_json


if __name__ == '__main__':
    print(main(sys.argv[1:]))
