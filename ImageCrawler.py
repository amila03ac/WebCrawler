
import re
import time
import urllib2
import logging
import urlparse
from bs4 import BeautifulSoup
from xml.etree.cElementTree import ElementTree
import xml.etree.ElementTree as ET
from StatXMLReader import readImgXML
from StatXMLReader import readMetaXML
from ImageAnalyzer import countImages
from werkzeug.debug.tbtools import PAGE_HTML

def crawlLinks(WebURL, limit):
    
    urlCount = 0
    imgCount = 0
    imgAll = 0
    domainList = dict()
    blockedDomains = list()
    WebURL=verifyUrl(WebURL)
    
    UrlList=set([WebURL])
    crawled = set([])
    linkregex = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')
    
    statroot=readImgXML("BlahBlah")
    metaroot=readMetaXML("BlahBlah")
    
    totPages = int(statroot.get('pagecount'))
    totPagesMeta = int(metaroot.get('pagecount'))
    
    for x in range(0, limit):
        try:
            if(len(UrlList) == 0):
                break
            crawling = UrlList.pop()
            urlDomain = urlparse.urlparse(crawling)[1]
            if(not urlDomain in blockedDomains):
       #        print(crawling)
                try:
                    response = urllib2.urlopen(crawling)
                except:
                    continue        
                msg = response.read()
                soup = BeautifulSoup(msg)
                
                print"Crawling>>"+ crawling
                
                images = soup.findAll("img")
#                 print(page_images)
#                 for x in range(0, len(page_images)):
#                     page_images[x] = urlparse.urljoin(crawling, page_images[x])
# #                 print(page_images)
                imgsall = len(images)
                print "all imgs: " + str(imgsall)
                imgs = countLrgImages(crawling, images, 64)                            
                
                imgCount += imgs
                imgAll += imgsall
                urlCount += 1
                
                crawled.add(crawling)
                print"| All img: "+str(imgsall) + "  |  Important img: " + str(imgs) +" |"
                
                totPages += 1;
                statroot.set("pagecount",str(totPages))
                
                statroot[0].text = str(int(statroot[0].text) + imgsall)
                statroot[1].text = str(int(statroot[1].text) + imgs)
                
                statDoc=ElementTree(statroot) 
                statDoc.write('output/data/imgStats.xml')
                
                
                """Store meta description in meta.xml"""
                data = soup.find("meta", attrs={'name':re.compile("^description$", re.I)})
#                 print (data)
                if(data is not None):
#                     print(data['content'])
                    metadata = data['content'];
                else:
                    metadata = ''
                
                newnode = ET.Element('webpage')
                newnode.set('url', str(crawling))
                newnode.set('description', str(metadata))
                metaroot.insert(0, newnode)
                
                totPagesMeta += 1;
                metaroot.set("pagecount",str(totPagesMeta))
                
                Doc=ElementTree(metaroot) 
                Doc.write('output/data/meta.xml')
                    
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
                    if(domainList[urlDomain] > 3):
                        blockedDomains.append(urlDomain)
                        del domainList[urlDomain]
                else:
                    domainList[urlDomain] = 1
                print(domainList)
                print(blockedDomains)
        except Exception, e: 
            print e
            continue
   
    print"-------------------------------------------------------------------\nSession Summary"
    print"Pages Crawled:       "+ str(urlCount)
    print"Total Images:        "+ str(imgAll)
    print"Important Images:    "+ str(imgCount)

    
    
    
    return True

def countLrgImages(siteurl, images, THRESHOLD):
#         print(images)
        largeImgCount = 0
        page_images = list()
        for img in images:
            w = int(re.match(r'\d+', img.attrs['width']).group() if 'width' in img.attrs else -1)
            h = int(re.match(r'\d+', img.attrs['height']).group() if 'height' in img.attrs else -1)
#             print(str(w) )
            if(w > THRESHOLD or h > THRESHOLD):
                largeImgCount += 1
            elif(w < 0 or h < 0):
                page_images.append(urlparse.urljoin(siteurl, img['src']))
                
#         for x in range(0, len(page_images)):
#             page_images[x] = urlparse.urljoin(siteurl, page_images[x])
        largeImgCount += countImages(page_images, THRESHOLD)
#         print("Images: " +str(imgCount) + "Large Images: " + str(largeImgCount))
        return largeImgCount

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