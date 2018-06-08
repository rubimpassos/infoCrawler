class Extractor:
    def __init__(self, element):
        """
        Extract elements by type that can be serialized
        p = text
        div>img = image
        div>ul = links
        :param element: A html parsed by BeautifulSoup
        :type element: BeautifulSoup object
        """
        self.element = element
        self._type, self.content = self.extract()

    def is_image(self):
        return self.element.name and self.element.img

    def is_text(self):
        return self.element.name == 'p'

    def is_links(self):
        return self.element.name and self.element.ul

    def extract(self):
        _type = ""

        if self.is_image():
            _type = "image"

        if self.is_text():
            _type = "text"

        if self.is_links():
            _type = "links"

        method = getattr(self, "_extract_"+_type, None)
        if not callable(method):
            return "", ""

        return _type, method()

    def _extract_image(self):
        return self.element.img['src']

    def _extract_text(self):
        text = self.element.text or ""
        return text.strip()

    def _extract_links(self):
        links = []
        for link in self.element.find_all('a'):
            links.append(link.get('href'))

        return links

    def as_dict(self):
        if not self.content or not self._type:
            return {}

        return {'type': self._type, 'content': self.content}
