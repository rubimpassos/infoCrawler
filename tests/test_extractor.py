from unittest import TestCase

from bs4 import BeautifulSoup

from rsscrawler.extractor import Extractor


class ExtractorTest(TestCase):
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

    def test_extract_image(self):
        extractor = self._get_element_extractor(self.image_html, 'div')

        expected = "http://www.exemple.org/image.jpg"
        type_, content = extractor.extract()

        self.assertEqual(expected, content)
        self.assertEqual("image", type_)

    def test_extract_text(self):
        extractor = self._get_element_extractor(self.text_html, 'p')

        expected = "Exemple of captured text"
        type_, content = extractor.extract()

        self.assertEqual(expected, content)
        self.assertEqual("text", type_)

    def test_extract_links(self):
        extractor = self._get_element_extractor(self.links_html, 'div')

        expected = ["http://www.exemple.org", "http://www.google.com", "http://www.facebook.com"]
        type_, content = extractor.extract()

        self.assertListEqual(expected, content)
        self.assertEqual("links", type_)
