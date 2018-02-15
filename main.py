import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *


# chosen random website from Wrexham, "dragon field sports"
# 'http://www.dragonfieldsports.co.uk/'
PROJECT_NAME = 'armoorhogs1'
HOMEPAGE = 'https://www.ardmoor.co.uk/hoggs-of-fife'
DOMAIN_NAME = 'https://www.ardmoor.co.uk/hoggsoffife'
# DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8  # this should be dependant on the OS
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)  # initial spider for the homepage, other will be threaded


# create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True  # runs as daemon, causes it to die when main thread exits
        t.start()


# do the next job in queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# each queued link is in the job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# check if there are items in the to do list and if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


create_workers()
crawl()