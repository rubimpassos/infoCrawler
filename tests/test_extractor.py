from unittest import TestCase
from bs4 import BeautifulSoup
from rsscrawler.extractor import Extractor


class ExtractorTest(TestCase):
    def _get_element_extractor(self, html, tag):
        soup = BeautifulSoup(html, "html.parser")
        return Extractor(soup.find(tag))

    def test_extract_image(self):
        html = '<div><img src="http://www.exemple.org/image.jpg" alt="Exemple Image" /></div>'
        extractor = self._get_element_extractor(html, 'div')

        expected = "http://www.exemple.org/image.jpg"
        type_, content = extractor.extract()

        self.assertEqual(expected, content)
        self.assertEqual("image", type_)

    def test_extract_text(self):
        html = '<p>Exemple of captured text</p>'
        extractor = self._get_element_extractor(html, 'p')

        expected = "Exemple of captured text"
        type_, content = extractor.extract()

        self.assertEqual(expected, content)
        self.assertEqual("text", type_)

    def test_extract_links(self):
        html = """
        <div>
            <ul>
                <li><a href="http://www.exemple.org" alt="exemple" >exemple</a></li>
                <li><a href="http://www.google.com" alt="google" >google</a></li>
                <li><a href="http://www.facebook.com" alt="facebook" >facebook</a></li>
            </ul>
        </div>
        """
        extractor = self._get_element_extractor(html, 'div')

        expected = ["http://www.exemple.org", "http://www.google.com", "http://www.facebook.com"]
        type_, content = extractor.extract()

        self.assertListEqual(expected, content)
        self.assertEqual("links", type_)
