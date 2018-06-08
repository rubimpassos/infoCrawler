import json
import os
from pathlib import Path
from unittest import TestCase

import mock
from bs4 import BeautifulSoup

from rsscrawler.crawler import parse_feed, parse_item, parse_description, feed_reader


class CrawlerTest(TestCase):
    @classmethod
    def setUpClass(cls):
        base_dir = Path(__file__).parent
        cls.path_xml_fixture = os.path.join(base_dir, "feed.xml")
        cls.path_json_fixture = os.path.join(base_dir, "feed.json")

        cls.xml_text_fixture = Path(base_dir, "feed.xml").read_text(encoding='utf-8')
        cls.xml_soup = BeautifulSoup(cls.xml_text_fixture, "xml")

        f = Path(base_dir, "feed.json").open(encoding='utf-8')
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

    # @mock.patch('requests.Session.get')
    # def test_feed_reader(self, mock_get):
    #     mock_get.return_value = mock.Mock(status=200, content=self.xml_text_fixture, json_data=None)
    #     expected = json.dumps(self.json_dict)
    #     json_string = feed_reader('some url')
    #     self.assertEqual(expected, json_string)
