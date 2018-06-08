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
        cls.json_dict_fixture = json.load(f)
        cls.feed_items = cls.json_dict_fixture.get('feed')

        cls.description = cls.xml_soup.item.description.text
        cls.descr_soup = BeautifulSoup(cls.description, "html.parser")

    def test_parsed_description(self):
        expected_desc_dict = self.feed_items[0]['description']
        result_desc_dict = parsed_description(self.description)

        self.assertEqual(expected_desc_dict, result_desc_dict)

    def test_parse_item(self):
        expected_item_dict = self.feed_items[0]
        xml_item = self.xml_soup.item
        result_item_dict = parse_item(xml_item)

        self.assertEqual(expected_item_dict, result_item_dict)

    def test_parse_feed(self):
        expected_feed_dict = parse_feed(self.xml_text_fixture)
        self.assertEqual(expected_feed_dict, self.json_dict_fixture)
