import sys
from MetaCrawler import crawl

url = sys.argv[1]
limit = int(sys.argv[2])
# url = "http://www.wired.com/"
# limit = 5
crawl(url, limit)