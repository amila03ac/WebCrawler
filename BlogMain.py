from BlogCrawler import BlogCrawler
from StatXMLReader import readXMLFile
# urlList = ['http://shahani-w.blogspot.com/', 'http://theframedtable.com/', 'http://sanjiva.weerawarana.org/', 'http://www.virtusa.com/blog/', 'http://www.huffingtonpost.com/', 'http://en.blog.wordpress.com/']
# urlList = ['http://www.theonion.com/']
# b = BlogCrawler()
# b.crawl(urlList)

urllist = list()
type = ''
urlxml = readXMLFile('input/nonblogLinks.xml')
for child in urlxml:
#     print child.text
    if(child.tag == 'info'):
        type = child[1].text
        continue
    urllist.append(child[0].text)
      
print urllist
 
b = BlogCrawler()
b.crawl(urllist, type)