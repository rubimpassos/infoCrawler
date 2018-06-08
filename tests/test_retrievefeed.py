from unittest import TestCase

import mock
from requests import HTTPError

from rsscrawler.retrivefeed import retrieve_feed


mock_response = mock.Mock(status=200, content='Test content', json_data=None)


class RetrieveFeedTest(TestCase):
    @mock.patch('requests.Session.get')
    def test_retrieve_feed_content(self, mock_get):
        expected_content = "Test content"
        mock_get.return_value = mock_response

        response = retrieve_feed('some url')
        self.assertEqual(expected_content, response)

    @mock.patch('requests.Session.get')
    def test_retrieve_feed_fail(self, mock_get):
        mock_response.status = 500
        mock_response.raise_for_status = mock.Mock(side_effect=HTTPError("Site is Down!"))
        mock_get.return_value = mock_response

        self.assertRaises(HTTPError, retrieve_feed, 'some url')
