import json
import os
from pathlib import Path
from unittest import TestCase

import mock
from bs4 import BeautifulSoup
from requests import HTTPError

from rsscrawler import crawler


class RetrieveFeedTest(TestCase):
    def _mock_response(self, status=200, content='CONTENT', json_data=None, raise_for_status=None):
        mock_resp = mock.Mock()

        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status

        mock_resp.status_code = status
        mock_resp.content = content

        if json_data:
            mock_resp.json = mock.Mock(return_value=json_data)

        return mock_resp

    @mock.patch('requests.Session')
    def test_retrieve_feed_content(self, mock_session):
        expected_content = "Test content"

        mock_response = self._mock_response(content=expected_content)
        session_instance = mock_session.return_value
        session_instance.get.return_value = mock_response

        response = crawler.retrieve_feed('some url')

        self.assertEqual(expected_content, response)
        session_instance.mount.assert_called()
        session_instance.get.assert_called_with('some url')

    @mock.patch('requests.Session')
    def test_retrieve_feed_fail(self, mock_session):
        mock_response = self._mock_response(status=500, raise_for_status=HTTPError("Rss Feed is down!"))
        session_instance = mock_session.return_value
        session_instance.get.return_value = mock_response

        self.assertRaises(HTTPError, crawler.retrieve_feed, 'some url')
        session_instance.mount.assert_called()
        session_instance.get.assert_called_with('some url')


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
        result_desc_dict = crawler.parsed_description(self.description)

        self.assertEqual(expected_desc_dict, result_desc_dict)

    def test_parse_item(self):
        expected_item_dict = self.feed_items[0]
        xml_item = self.xml_soup.item
        result_item_dict = crawler.parse_item(xml_item)

        self.assertEqual(expected_item_dict, result_item_dict)

    def test_parse_feed(self):
        expected_feed_dict = crawler.parse_feed(self.xml_text_fixture)
        self.assertEqual(expected_feed_dict, self.json_dict_fixture)
