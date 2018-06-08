class Extractor:
    valid_types = ('image', 'text', 'links')

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
        self.content_type = self.get_content_type()

    def get_content_type(self):

        if not self.element.name:
            return ''

        if self.element.name == 'p':
            return 'text'
        elif self.element.ul:
            return 'links'
        elif self.element.img:
            return 'image'

        return ""

    def is_valid(self):
        return self.content_type in self.valid_types

    def extract(self):
        if not self.is_valid():
            return ""

        method = getattr(self, "_extract_"+self.content_type, None)
        if not callable(method):
            return ""

        return method()

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
        if not self.is_valid():
            return {}

        content = self.extract()
        if not content:
            return {}

        return {'type': self.content_type, 'content': content}
