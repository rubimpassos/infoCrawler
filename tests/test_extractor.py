from unittest import TestCase
from bs4 import BeautifulSoup
from rsscrawler.extractor import Extractor


class ExtractorTest(TestCase):
    def test_extract_image(self):
        html = '<div><img src="http://www.exemple.org/image.jpg" alt="Exemple Image" /></div>'
        soup = BeautifulSoup(html, "html.parser")
        extractor = Extractor(soup.div)

        expected = "image", "http://www.exemple.org/image.jpg"

        self.assertEqual(expected, extractor.extract())

    def test_extract_text(self):
        html = '<p>Exemple of captured text</p>'
        soup = BeautifulSoup(html, "html.parser")
        extractor = Extractor(soup.p)

        expected = "text", "Exemple of captured text"

        self.assertEqual(expected, extractor.extract())

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
        soup = BeautifulSoup(html, "html.parser")
        extractor = Extractor(soup.div)

        expected = "links", ["http://www.exemple.org", "http://www.google.com", "http://www.facebook.com"]

        self.assertEqual(expected, extractor.extract())
