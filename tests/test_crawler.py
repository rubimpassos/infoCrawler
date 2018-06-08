import json
import os
from pathlib import Path
from unittest import TestCase

from bs4 import BeautifulSoup

from rsscrawler.crawler import parse_feed, parse_item, parse_description


class CrawlerTest(TestCase):
    @classmethod
    def setUpClass(cls):
        tests_path = os.path.dirname(os.path.realpath(__file__))
        cls.path_xml_fixture = os.path.join(tests_path, "feed.xml")
        cls.path_json_fixture = os.path.join(tests_path, "feed.json")

        cls.xml_text_fixture = Path(tests_path, "feed.xml").read_text(encoding='utf-8')
        cls.xml_soup = BeautifulSoup(cls.xml_text_fixture, "xml")

        f = Path(tests_path, "feed.json").open(encoding='utf-8')
        cls.json_dict = json.load(f)
        cls.feed_item = cls.json_dict['feed'][0]

    def test_parsed_description(self):
        description = self.xml_soup.item.description.text

        expected = self.feed_item['description']
        descr_contents = parse_description(description)

        self.assertEqual(expected, descr_contents)

    def test_parse_item(self):
        expected = self.feed_item
        xml_item = self.xml_soup.item
        item_contents = parse_item(xml_item)

        self.assertEqual(expected, item_contents)

    def test_parse_feed(self):
        expected = parse_feed(self.xml_text_fixture)
        self.assertEqual(expected, self.json_dict)
