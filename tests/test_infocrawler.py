import json
import os
from unittest import TestCase

from bs4 import BeautifulSoup

from info_crawler import extract_image_url, extract_text_content, extract_links, parsed_description, parse_item


class InfoCrawlerTest(TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.xml_path = os.path.join(dir_path, "feed.xml")
        self.json_path = os.path.join(dir_path, "feed.json")

        with open(self.xml_path, encoding='utf-8') as f:
            self.xml_soup = BeautifulSoup(f, "xml")

        with open(self.json_path, encoding='utf-8') as f:
            self.d_json = json.load(f)
            self.feed_items = self.d_json.get('feed')

    def test_extract_image_url(self):
        image_url = "http://www.exemple.org/image.jpg"
        html = '<img src="{}" alt="Exemple Image" />'.format(image_url)
        soup = BeautifulSoup(html, "html.parser")
        extracted_url = extract_image_url(soup.img)

        self.assertEqual(extracted_url, image_url)

    def test_extract_text_content(self):
        text = "Exemple of captured text"
        html = '<p>{}</p>'.format(text)
        soup = BeautifulSoup(html, "html.parser")
        extracted_text = extract_text_content(soup.p)

        self.assertEqual(extracted_text, text)

    def test_extract_links(self):
        links = [
            "http://www.exemple.org",
            "http://www.google.com",
            "http://www.facebook.com",
        ]
        html = """
        <ul>
            <li><a href="{}" alt="exemple" >exemple</a></li>
            <li><a href="{}" alt="google" >google</a></li>
            <li><a href="{}" alt="facebook" >facebook</a></li>
        </ul>
        """.format(*links)
        soup = BeautifulSoup(html, "html.parser")
        extracted_links = extract_links(soup.ul)

        self.assertListEqual(extracted_links, links)

    def test_parsed_description(self):
        j_content = self.feed_items.first().get('content')
        description = self.xml_soup.find('item').find('description').text
        extracted_content = parsed_description(description)

        self.assertEqual(str(extracted_content), str(j_content))

    def test_parse_item(self):
        j_item = self.feed_items[0]
        x_item = self.xml_soup.find('item')
        parsed_item = parse_item(x_item)

        self.assertEqual(str(parsed_item), str(j_item))
