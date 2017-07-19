from html.parser import HTMLParser

class HtmlFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def handle_starttag(self, tag, attributes):
        if tag == 'a':
            for(attribute, value) in attributes:
                if attribute == 'href' and value.find('http') is not -1:
                    self.links.add(value)

    def page_links(self):
        return self.links

    def error(self, message):
        print(message)

