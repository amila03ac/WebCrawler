import urllib2
from bs4 import BeautifulSoup
import urlparse
from external import getimageinfo
from urllib2 import HTTPError
import logging


#===============================================================================
# countImages
# Counts the number of images that are larger than a given Threshold.
# @param page_images: set of image uris
# @param Threshold: threshold
# @return: int imageCount
#===============================================================================
def countImages(page_images, THRESHOLD):
        
    count = 0
    for uri in page_images:
        try:
            imgdata = urllib2.urlopen(uri)
        except Exception, e:
            print(">>>>>>>>"+ str(uri) +"<<<<<<<<")
            print(e)
            continue
        image_type,width,height = getimageinfo.getImageInfo(imgdata)        
        if(width>THRESHOLD or height>THRESHOLD):
            count += 1
    return count

#===============================================================================
# countImagesFromSite
# Counts the number of images that are larger than a given Threshold in a given website.
# @param siteurl: url of the web site
# @param Threshold: threshold
# @return: int imageCount
#===============================================================================
def countImagesFromSite(siteurl, THRESHOLD):
    try:
        response = urllib2.urlopen(verifyUrl(siteurl))
    except:
        return 0        
    msg = response.read()
    soup = BeautifulSoup(msg)
                
    page_images = [image["src"] for image in soup.findAll("img")]
#     print(page_images)
    for x in range(0, len(page_images)):
        page_images[x] = urlparse.urljoin(siteurl, page_images[x])
    
    return countImages(page_images, THRESHOLD)

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