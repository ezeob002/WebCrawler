import threading
from queue import Queue
from crawler import Crawler
from general import *
import sys

# Setup global variables for the project

NUMBER_OF_THREADS = 16
queue = Queue()


# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Crawler.crawl_page(url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in Crawler.queue_set:
        queue.put(link)
    queue.join()
    crawl() # to get the updated version of the queue


# Check if there are items in the queue, if so crawl them
def crawl():
    if len(Crawler.queue_set) > 0:
        create_jobs()


def main():
    if len(sys.argv) < 2:
        sys.stderr.write('E: usage ' + sys.argv[0] + ' <filename\>')
        sys.stderr.flush()
        exit(2)
    home_page = sys.argv[1]
    project_name = 'Results'
    domain_name = General.get_domain_name(home_page)
    Crawler(home_page, domain_name, project_name)
    create_workers()
    crawl()


main()
