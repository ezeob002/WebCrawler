from urllib.request import urlopen
from htmlFinder import HtmlFinder
from general import *
from threading import Lock


class Crawler:
    # It will be visible to all Threads, static variables for multi-threading
    base_url = ''
    domain_name = ''
    result_file = ''
    project_name = ''
    queue_set = set()
    crawled_set = set()
    lock = Lock()

    def __init__(self, base_url, domain_name, project_name):
        Crawler.base_url = base_url
        Crawler.domain_name = domain_name
        Crawler.project_name = project_name
        Crawler.result_file = project_name + '/result.txt'
        Crawler.start()
        Crawler.queue_set.add(Crawler.base_url)
        Crawler.crawl_page(Crawler.base_url)

    @staticmethod
    def start():
        General.create_project_dir(Crawler.project_name)
        General.create_data_files(Crawler.project_name)
    @staticmethod
    def crawl_page(page_url):
        if page_url not in Crawler.crawled_set:
            Crawler.add_links_to_queue(Crawler.gather_links(page_url), page_url)
            Crawler.queue_set.remove(page_url)
            Crawler.crawled_set.add(page_url)

    # Connect to sites, take the html converts to a string html, it passes it to the linker finder and gets back all
    # the urls
    @staticmethod
    def gather_links(page_url):
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = HtmlFinder(Crawler.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            #print(str(e))
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links, page_url):
        Crawler.lock.acquire()
        print(page_url)
        General.append_to_file(Crawler.result_file,page_url)
        for url in links:
            if (url in Crawler.queue_set) or (url in Crawler.crawled_set) or (
                        Crawler.domain_name != General.get_domain_name(url)):
                continue
            Crawler.queue_set.add(url)
            # prints the url to the log
            print('  ', url)
            General.append_to_file(Crawler.result_file, '  ' + url)
        print()
        Crawler.lock.release()

