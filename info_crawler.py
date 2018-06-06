import json
import xmltodict
from bs4 import BeautifulSoup


def parsed_description(description):
    soup = BeautifulSoup(description, "html.parser")
    content = []
    for el in soup:
        if el.name == 'div':
            if el.img:
                content.append({
                    'type': "image",
                    'content': el.img['src']
                })
            # verifico se existe a organização div<ul<li<a
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


with open('feed.xml', encoding='utf-8') as xml_feed:
    xml_dict = xmltodict.parse(xml_feed.read())
    item = xml_dict.get('item', {})

output = {}
for k, v in item.items():
    if k in ['title', 'link']:
        output[k] = v
        continue

    if k == "description":
        output['content'] = parsed_description(v)

feed_json = json.dumps(output)
print(feed_json)

