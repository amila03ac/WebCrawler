import sys
from ImageCrawler import crawlLinks

url = sys.argv[1]
limit = int(sys.argv[2])
# url = "http://www.harpers.org"
# limit = 5
crawlLinks(url, limit)