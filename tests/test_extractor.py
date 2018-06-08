from unittest import TestCase

from bs4 import BeautifulSoup

from rsscrawler.extractor import Extractor


class ExtractTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.image_html = '<div><img src="http://www.exemple.org/image.jpg" alt="Exemple Image" /></div>'
        cls.text_html = '<p>Exemple of captured text</p>'
        cls.links_html = """
        <div>
            <ul>
                <li><a href="http://www.exemple.org" alt="exemple" >exemple</a></li>
                <li><a href="http://www.google.com" alt="google" >google</a></li>
                <li><a href="http://www.facebook.com" alt="facebook" >facebook</a></li>
            </ul>
        </div>
        """

    def _get_element_extractor(self, html, tag):
        soup = BeautifulSoup(html, "html.parser")
        return Extractor(soup.find(tag))

    def test_description_content_type_image(self):
        extractor = self._get_element_extractor(self.image_html, 'div')
        self.assertEqual("image", extractor.content_type)

    def test_description_content_type_text(self):
        extractor = self._get_element_extractor(self.text_html, 'p')
        self.assertEqual("text", extractor.content_type)

    def test_description_content_type_links(self):
        extractor = self._get_element_extractor(self.links_html, 'div')
        self.assertEqual("links", extractor.content_type)

    def test_extract_image(self):
        extractor = self._get_element_extractor(self.image_html, 'div')

        expected = "http://www.exemple.org/image.jpg"
        url = extractor.extract()

        self.assertEqual(expected, url)

    def test_extract_text(self):
        extractor = self._get_element_extractor(self.text_html, 'p')

        expected = "Exemple of captured text"
        text = extractor.extract()

        self.assertEqual(expected, text)

    def test_extract_links(self):
        extractor = self._get_element_extractor(self.links_html, 'div')

        expected = ["http://www.exemple.org", "http://www.google.com", "http://www.facebook.com"]
        links = extractor.extract()

        self.assertListEqual(expected, links)

    def test_image_extractor_as_dict(self):
        extractor = self._get_element_extractor(self.image_html, 'div')

        expected = {'type': 'image', 'content': 'http://www.exemple.org/image.jpg'}
        d = extractor.as_dict()

        self.assertEqual(expected, d)

    def test_text_extractor_as_dict(self):
        extractor = self._get_element_extractor(self.text_html, 'p')

        expected = {'type': 'text', 'content': 'Exemple of captured text'}
        d = extractor.as_dict()

        self.assertEqual(expected, d)

    def test_links_extractor_as_dict(self):
        extractor = self._get_element_extractor(self.links_html, 'div')

        expected = {
            'type': 'links',
            'content': ["http://www.exemple.org", "http://www.google.com", "http://www.facebook.com"]
        }
        d = extractor.as_dict()

        self.assertEqual(expected, d)
