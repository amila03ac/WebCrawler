import re
import urllib2
import urlparse
from bs4 import BeautifulSoup
from urllib2 import URLError
from HTMLStripper import strip_tags

#===============================================================================
# crawl
# Given a base url and a limit this method will crawl web pages until the limit
# is reached. It will check for 'meta-keywords' and 'meta-description' within 
# a web page and store the details. A maximum of 3 web pages will be crawled in
# a single domain.
# @param baseurl: starting url 
# @param limit: limit specify the number of web pages to crawl
#===============================================================================
def crawl(baseurl, limit):
    
    domainList = dict()
    blockedDomains = list()
    WebURL=verifyUrl(baseurl)
    UrlList=set([WebURL])
    crawled = set([])
    linkregex = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')
    
    with open('output/data/meta_data_raw.xml', 'a') as metafile:
        for x in range(0, limit):
            try:
                if(len(UrlList) == 0):
                    print ">>>No more links :( <<<"
                    break
                crawling = UrlList.pop()
                urlDomain = urlparse.urlparse(crawling)[1]
                if(not urlDomain in blockedDomains):
                    print(">>>"+ str(x) + ": " + crawling)
                    try:
                        response = urllib2.urlopen(crawling, timeout=20)
                    except URLError, err:
                        print(err)
                        continue        
                    msg = response.read()
                    soup = BeautifulSoup(msg)
                    
                    print">>>Crawling>>"+ crawling
                    
                    crawled.add(crawling)                    
                    
                    """Store meta description in meta.xml"""
                    description = soup.find("meta", attrs={'name':re.compile("^description$", re.I)})
                    keywords = soup.find("meta", attrs={'name':re.compile("^keywords$", re.I)})
    #                 print (description)
                    if(description is not None):
    #                     print(description['content'])
                        metadescription = description['content'];
                    else:
                        metadescription = ''
                    
                    if(keywords is not None):
    #                     print(description['content'])
                        metakeywords = keywords['content'];
                    else:
                        metakeywords = ''
                    
                    metadescription = metadescription.replace('"', '')
                    metakeywords = metakeywords.replace('"', '')
                    metadescription = str(strip_tags(metadescription))
                    metakeywords = str(strip_tags(metakeywords))
                    webpagemeta = '<webpage url="'+str(crawling)+'" keywords="'+metakeywords+'" description="'+metadescription+'" />'
                    webpagemeta = str(webpagemeta)
                    webpagemeta = webpagemeta.replace('&', '&amp;')
#                     print(webpagemeta)
                    metafile.write(webpagemeta)
                    metafile.flush()
                        
                    """Get all links from the current web page and add them to the list"""
    #                 print"getting links"
                    links = linkregex.findall(msg)
                    print "got links in "+ crawling
                    print(len(links))
                    for link in links:
            
                        if link.startswith('#'):
                            crawled.add(urlparse.urljoin(crawling, link))
                            continue
                        else:
                            link = urlparse.urljoin(crawling, link);
                        if(link not in crawled):
                            UrlList.add(link)
                    
                    """Check if a particular domain has exceeded the web page limit"""
                    if(urlDomain in domainList):
                        domainList[urlDomain] = domainList[urlDomain] +1
                        if(domainList[urlDomain] > 2):
                            blockedDomains.append(urlDomain)
                            del domainList[urlDomain]
                    else:
                        domainList[urlDomain] = 1
                    #print(domainList)
                    #print(blockedDomains)
            except Exception, e: 
                print e
                continue
    return True

#===============================================================================
# verifyUrl
# Adds 'http://' the the begining of a url.
# @param weblink: url
# @return: new url
#===============================================================================
def verifyUrl(weblink):
    if not weblink.startswith('http://'):
        weblink = 'http://' + weblink 
    return weblink