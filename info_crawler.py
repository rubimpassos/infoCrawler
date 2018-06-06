import json
import sys

import requests
import xmltodict

from bs4 import BeautifulSoup
from xml.parsers.expat import ExpatError


def parsed_description(description):
    """Returns images, links and paragraphs of the description
    :rtype: dict
    """
    soup = BeautifulSoup(description, "html.parser")
    content = []
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


def read_xml(url):
    """Returns the xml data from url
    :rtype: dict
    """
    reponse = requests.get(url)
    xml_dict = {}

    if reponse.status_code == 200:
        try:
            xml_dict = xmltodict.parse(reponse.content)
        except ExpatError:
            pass

    return xml_dict


def main(arg):
    xml = read_xml("https://revistaautoesporte.globo.com/rss/ultimas/feed.xml")

    feed = {'feed': []}
    valid_fields = ['title', 'link', 'description']

    #
    if 'rss' in xml and 'channel' in xml.get('rss', {}):
        channel = xml['rss'].get('channel', {})
        items = channel.get('item', [])
        for info in items:
            # clean nonessential fields
            invalid_fields = list(set(info.keys()) - set(valid_fields))
            for field in invalid_fields:
                info.pop(field, None)

            if valid_fields[2] in info:
                info['content'] = parsed_description(info[valid_fields[2]])
                info.pop(valid_fields[2], None)

            feed['feed'].append(info)

    feed_json = json.dumps(feed, ensure_ascii=False, indent=True)
    print(feed_json)


if __name__ == '__main__':
    main(sys.argv[1:])
