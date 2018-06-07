import json
import os
from unittest import TestCase

import info_crawler

from bs4 import BeautifulSoup


class InfoCrawlerTest(TestCase):
    @classmethod
    def setUpClass(cls):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        cls.xml_path = os.path.join(dir_path, "feed.xml")
        cls.json_path = os.path.join(dir_path, "feed.json")

        with open(cls.xml_path, encoding='utf-8') as f:
            cls.xml_text = f.read()
            cls.xml_soup = BeautifulSoup(cls.xml_text, "xml")

        with open(cls.json_path, encoding='utf-8') as f:
            cls.d_json = json.load(f)
            cls.feed_items = cls.d_json.get('feed')

    def test_retrieve_feed_content(self):
        rss_url = "https://revistaautoesporte.globo.com/rss/ultimas/feed.xml"
        content = info_crawler.retrieve_feed(rss_url)

        self.assertIsInstance(content, bytes)

    def test_extract_image_url(self):
        image_url = "http://www.exemple.org/image.jpg"
        html = '<img src="{}" alt="Exemple Image" />'.format(image_url)
        soup = BeautifulSoup(html, "html.parser")
        extracted_url = info_crawler.extract_image_url(soup.img)

        self.assertEqual(extracted_url, image_url)

    def test_extract_text_content(self):
        text = "Exemple of captured text"
        html = '<p>{}</p>'.format(text)
        soup = BeautifulSoup(html, "html.parser")
        extracted_text = info_crawler.extract_text_content(soup.p)

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
        extracted_links = info_crawler.extract_links(soup.ul)

        self.assertListEqual(extracted_links, links)

    def test_parsed_description(self):
        j_content = self.feed_items[0].get('description')
        description = self.xml_soup.find('item').find('description').text
        extracted_content = info_crawler.parsed_description(description)

        self.assertEqual(str(extracted_content), str(j_content))

    def test_parse_item(self):
        j_item = self.feed_items[0]
        x_item = self.xml_soup.find('item')
        parsed_item = info_crawler.parse_item(x_item)

        self.assertEqual(str(parsed_item), str(j_item))

    def test_parse_feed(self):
        d_feed = info_crawler.parse_feed(self.xml_text)
        self.assertEqual(str(d_feed), str(self.d_json))
