import unittest
from BlogCrawler import BlogCrawler
from bs4 import BeautifulSoup

class WebCrawlerTest(unittest.TestCase):
    
    l1 = '<html><head>'
    l2 = '<link href="http://shahani-w.blogspot.com/favicon.ico" rel="icon" type="image/x-icon"/>'
    l3 = '<link rel="alternate" type="application/atom+xml" title="Shahani Perspectives - Atom" href="http://shahani-w.blogspot.com/feeds/posts/default" />'
    l4 = '<link rel="alternate" type="application/rss+xml" title="Shahani Perspectives - RSS" href="http://shahani-w.blogspot.com/feeds/posts/default?alt=rss" />'
    l5 = '<link rel="service.post" type="application/atom+xml" title="Shahani Perspectives - Atom" href="http://www.blogger.com/feeds/8962408196508320634/posts/default" />'
    l6 = '</head></html>'
    
    htmlWithRss = l1+l2+l3+l4+l5+l6
    htmlWithoutRss = l1+l2+l6
    crawler = BlogCrawler()
    
    def testCheckFeedWithRss(self):
        head = BeautifulSoup(self.htmlWithRss)
        result = self.crawler.checkFeed(head)
        self.assertEqual(True, result)
        
    def testCheckFeedWithOutRss(self):
        head = BeautifulSoup(self.htmlWithoutRss)
        result = self.crawler.checkFeed(head)
        self.assertEqual(False, result)
        
    
    
    if __name__ == "__main__":
        unittest.main()  