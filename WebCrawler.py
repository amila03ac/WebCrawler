'''
Created on Jan 31, 2013

@author: Anghiari
'''

import re
import urllib2
import logging
import urlparse
from bs4 import BeautifulSoup
from xml.etree.cElementTree import ElementTree
from xml.etree.ElementTree import SubElement, Element
from StatXMLReader import readXML
import time
from ImageAnalyzer import countImages
'''
@summary: crawlLinks takes the URL of a webpage and crawls all the links in that page and its child pages. 
The pages are saved at the source folder named with the web page URL.

@param WebURL: The URL of the parent web page to be crawled.
@param limit: The number of webpages to be crawled.  
'''   
def crawlLinks(WebURL,limit):

    count = 0
    component = ""
    webtag=""
    count = 0
    WebURL=verifyUrl(WebURL)
#    makeDirectory(urlparse.urlparse(WebURL)[1])
    
    
    stats=list()
    
    UrlList=set([WebURL])
    crawled = set([])
    keywordregex = re.compile('<meta\sname=["\']keywords["\']\scontent=["\'](.*?)["\']\s/>')
    linkregex = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')
   
    
    root=readXML("filepath")
        
    k=0 
    elementcount = []
    for stat in root.findall('stat'):
        elementcount.append(0)
        
    for x in range(0, limit):
        try:
            crawling = UrlList.pop()
            print "%d - URL Crawling -- "%x+crawling
            logging.info("%d - URL Crawling -- "%x+crawling)
            
        except KeyError:
            print KeyError.message
            return False
        
        url = urlparse.urlparse(crawling)
        
        try:
            response = urllib2.urlopen(crawling)
        except:
            continue
        
        msg = response.read()
        soup = BeautifulSoup(msg)
        
        if(soup.title!=None):
            title = soup.title.text
        else:
            title="NO TITLE"
        
        #print "Webpage Title--" +title
        #logging.info("Webpage Title--" +title)

#        print "Webpage Title--" +title
        #logging.info("Webpage Title--" +title)
                
        keywordlist = keywordregex.findall(msg)
        
        if len(keywordlist) > 0:
            keywordlist = keywordlist[0]
            keywordlist = keywordlist.split(", ")
            
        links = linkregex.findall(msg)
        
        
        ######################output.xml#######################################
        data = Element('xml')
        
        info= SubElement(data, 'info')
        
        ##details start
        details=SubElement(info, 'details')
        
        webPages=SubElement(details, 'webpages')
        
        localtime = time.asctime( time.localtime(time.time()) )
        date=SubElement(details, 'date')
        date.text = localtime
        
        ##details end
        
        ##elements start
        elements=SubElement(info, 'elements')        
        doc = ElementTree(data)  
        #elements end
        ######################output.xml#######################################
        
        ######################total.xml#######################################
        totalData = Element('xml')
        
        totalInfo= SubElement(totalData, 'info')
        
        ##details start
        totalDetails=SubElement(totalInfo, 'details')
        
        totalWebPages=SubElement(totalDetails, 'webpages')
        
        totalLocaltime = time.asctime( time.localtime(time.time()) )
        totalDate=SubElement(totalDetails, 'date')
        totalDate.text = totalLocaltime
        
        ##details end
        
        ##elements start
        totalElements=SubElement(totalInfo, 'elements')        
        totalDoc = ElementTree(totalData)  
        #elements end
        ######################output.xml####################################### 
         
        j=0

        loggerstring = ""
        
        for stat in root.findall('stat'):
            webtag = stat.get('webtag')
            component = stat.get('component')
            if(webtag == "img"):
                print "calling ImageAnalyzer"
                pageCount = countImages(crawling, 64)
            else:
                pageCount=len(soup.find_all(webtag))
            elementcount[j] += pageCount
            loggerstring +=  component+"-"+ str(pageCount)+" | "
            
            if(k==0):
                stats.append(int(stat.text)+pageCount)
            else:
                stats[j]+=pageCount
            createXMLGroup(component, elementcount[j], elements)
            j+=1
        
        print elementcount
        logging.info("Page Elements = " +loggerstring)
        loggerstring = ""
           
        k=1
        
        crawled.add(crawling)
        count+=1
        webPages.text = "%d" %count
        for link in (links.pop(0) for _ in xrange(len(links))):
            if link.startswith('/'):
                link = 'http://' + url[1] + link
            elif link.startswith('#'):
                crawled.add(link)
                continue
            if link not in crawled:
                UrlList.add(link)
                
        print "Moving to the next"
        logging.info("-------------------------------------------")
        
        doc.write("output/data/output.xml", "us-ascii", None, None, "xml")
    #saveAsHtmlPage("stats", "statistics", doc.write_c14n(file))
    
        i=0
        for stat in root.findall('stat'):
            stat.text=str(stats[i])
            component = stat.get('component')
            tagPageCount=int(stat.get('pagecount'))+count  
            createTotalXMLGroup(component, stats[i], tagPageCount,totalElements)
            i=i+1
        currentPageCount=int(root.get('pagecount'))+count
        totalWebPages.text = "%d" %currentPageCount
        totalDoc.write("output/data/total.xml", "us-ascii", None, None, "xml")
        
    for stat in root.findall('stat'):
            tagPageCount=int(stat.get('pagecount'))+count
            stat.set("pagecount",str(tagPageCount))
    pagecount=int(root.get('pagecount'))+count 
    root.set("pagecount",str(pagecount))
    
 

    statDoc=ElementTree(root) 
    statDoc.write('output/data/stats.xml')
    return True


def verifyUrl(weblink):
    if not weblink.startswith('http://'):
        weblink = 'http://' + weblink 
    return weblink
    
def createXMLGroup(eleType,count,parentEle):
    
    element=SubElement(parentEle,'element')
    typeElement=SubElement(element, 'type')
    typeElement.text=eleType
    
    countElement=SubElement(element, 'count')
    countElement.text="%d" %count
    
    return element


def createTotalXMLGroup(eleType,count,pageCount,parentEle):
    
    element=SubElement(parentEle,'element')
    typeElement=SubElement(element, 'type')
    typeElement.text=eleType
    
    countElement=SubElement(element, 'count')
    countElement.text="%d" %count
    
    pageCountElement=SubElement(element, 'pageCount')
    pageCountElement.text="%d" %pageCount
    
    return element
    