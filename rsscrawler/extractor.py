class Extractor:
    def __init__(self, element):
        self.element = element

    def extract(self, _type):
        method = getattr(self, "_extract_"+_type, None)

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

    @property
    def content_type(self):
        if not self.element.name:
            return ''

        if self.element.name == 'p':
            return 'text'
        elif self.element.ul:
            return 'links'
        elif self.element.img:
            return 'image'

        return ''
