class Extractor:
    """
    Extract elements by type that can be serialized
    p = text
    div>img = image
    div>ul = links
    :param element: A html parsed by BeautifulSoup
    :type element: BeautifulSoup object
    """
    def __init__(self, element):
        self.element = element

    def extract(self):
        type_, content = "", ""

        if self.is_image():
            type_ = "image"
            content = self.extract_image()

        elif self.is_text():
            type_ = "text"
            content = self.extract_text()

        elif self.is_links():
            type_ = "links"
            content = self.extract_links()

        return type_, content

    def is_image(self):
        return self.element.name == 'div' and self.element.img

    def extract_image(self):
        return self.element.img['src']

    def is_text(self):
        return self.element.name == 'p'

    def extract_text(self):
        text = self.element.text or ""
        return text.strip()

    def is_links(self):
        return self.element.name == 'div' and self.element.ul

    def extract_links(self):
        links = []
        for link in self.element.find_all('a'):
            links.append(link.get('href'))

        return links
