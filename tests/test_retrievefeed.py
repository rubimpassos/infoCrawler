from unittest import TestCase

import mock
from requests import HTTPError

from rsscrawler.retrivefeed import retrieve_feed


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

        response = retrieve_feed('some url')
        self.assertEqual(expected_content, response)

    @mock.patch('requests.Session')
    def test_retrieve_feed_fail(self, mock_session):
        mock_response = self._mock_response(status=500, raise_for_status=HTTPError("Rss Feed is down!"))
        session_instance = mock_session.return_value
        session_instance.get.return_value = mock_response

        self.assertRaises(HTTPError, retrieve_feed, 'some url')