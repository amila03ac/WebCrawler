import re
import urllib2
import urlparse
from bs4 import BeautifulSoup, Comment
from urllib2 import URLError
import BlogAnalyser
import ImageAnalyzer

class BlogCrawler:
    IMAGE_THRESHOLD = 92
    BLOG = 'blog'
    FORUM = 'forum'
    LINK_REGEX = '<a\s*href=[\'|"](.*?)[\'"].*?>'
    FORUM_FREQUENT_WORDS = ['thread ', 'topic ', 'forum ', 'posts ', 'views ', 'replies ', 'community ']
    ORGANIZATION_FREQUENT_WORDS = ['contact us', 'careers', 'products', 'solutions']
    
    #===========================================================================
    # crawl
    # Given a list of urls this method will crawl each url and extract the following features.
    # 1. Paragraph count
    # 2. Small Paragraph count
    # 3. Word count
    # 4. Image count
    # 5. Large image count (large image => width or height > a fixed threshold
    # 6. Internal/External link count
    # 7. Metadata availability (metakeywords, metadiscription)
    # 8. word 'blog' in metadata/url
    # 9. has Feed links
    # 10. has comments section
    # 11. Image to paragraph ratio
    # 12. Word to paragraph ratio
    # 
    # @param urlList: a list of urls
    # @param type: the type (Blog ot nonBlog) of the set of urls
    #===========================================================================
    def crawl(self, urlList, type):

        stats = {'paraCount':0,'smallParaCount':0,'wordCount':0,'imgCount':0,
                 'largeImgCount':0,'internalLinks':0,'externalLinks':0,'hasMetaDis':False,
                 'hasMetaKeywords':False,'hasBlogWordInMetaData':False,'hasCommentBox':False,
                 'hasPostsArchive':False,'hasBlogWordInURL':False,'hasFeed':False,
                 'imgToParaRatio':0,'bothDisandKeyInMeta':False,'wordToParaRatio':0,
                 'bothCommentAndArchive':False,'intLinkToExtLinkRatio':0,'totLinks':0,
                 'hasForumWordInMetaData':False, 'tableCount':0, 'rowCount':0, 'rowToTableRatio':0,
                 'hasForumWordInURL':False, 'divCount':0, 'forumFreqWordCount':0, 'orgFreqWordCount':0}
        
        with open('output/data/feature_set_new_forum_added.xml', 'a') as featurefile:
            for url in urlList:
                
                try:
#                     response = urllib2.urlopen(url)
                    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36' }
                    req = urllib2.Request(url, None, headers)
                    # req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36')
                    response = urllib2.urlopen(req)
                    siteurl = response.geturl()
                                
                    if('?' in siteurl):
                        continue
                           
#                     soup = BeautifulSoup(response.read())    
                    soup = BeautifulSoup(response)                
                    
                    '''Remove Comments'''
                    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
                    [comment.extract() for comment in comments]
                    
                    '''Extract img tags'''
                    images = soup.findAll('img')
    #                 page_images = [image["src"] for image in images]
    #                 [img.extract() for img in images]
                    
                    '''Remove scripts,img,iframe and style tags'''
                    [s.extract() for s in soup(['script', 'img', 'iframe', 'style'])]
                    '''Extract <head>'''
                    head = soup.find('head')
                    head.extract()            
        #             print(head)
                    
                    '''Check "blog", "forum" in URL'''
                    stats['hasBlogWordInURL'], stats['hasForumWordInURL'] = self.checkURL(siteurl)
                    
                    '''Check for feed (rss, atom) links'''
                    stats['hasFeed'] = self.checkFeed(head)
                    
                    '''Check Metadata'''
                    stats['hasMetaDis'], stats['hasMetaKeywords'], stats['hasBlogWordInMetaData'], stats['hasForumWordInMetaData'] = self.checkMetaData(head)
                    
                    '''Count internal and external links'''
                    stats['internalLinks'], stats['externalLinks'] =self.countLinks(soup, siteurl)
                    
                    '''Check for comment section'''
                    stats['hasCommentBox'] = self.CheckCommentsSection(soup)
                    
                    '''Check for posts archive'''
                    stats['hasPostsArchive'] = BlogAnalyser.checkForArchiveList(soup)
                    
                    '''Count Words and Paragraphs'''
                    stats['paraCount'], stats['smallParaCount'], stats['wordCount'] = BlogAnalyser.countParaAndWord(soup)
                    
                    '''Count Images'''
    #                 stats['imgCount'], stats['largeImgCount'] = self.countImages(siteurl, page_images)
                    stats['imgCount'], stats['largeImgCount'] = self.countImages(siteurl, images)
                    
                    '''count tables and rows'''
                    stats['tableCount'], stats['rowCount'] = self.countTablesAndRows(soup)
                    
                    '''div count'''
                    stats['divCount'] = self.countDiv(soup)
                    
                    '''frequent word counts'''
                    stats['forumFreqWordCount'], stats['orgFreqWordCount'] = self.countFrequentWords(soup)
                    
                    stats['imgToParaRatio'] = round(stats['paraCount']/float(stats['largeImgCount']),2) if (stats['paraCount']>0 and stats['largeImgCount']>0) else 0
                    stats['bothDisandKeyInMeta'] = stats['hasMetaDis'] and stats['hasMetaKeywords']
                    stats['wordToParaRatio'] = round(stats['wordCount']/float(stats['paraCount']),2) if (stats['wordCount']>0 and stats['paraCount']>0) else 0
                    stats['bothCommentAndArchive'] = stats['hasCommentBox'] and stats['hasPostsArchive']
                    stats['intLinkToExtLinkRatio'] = round(stats['internalLinks']/float(stats['externalLinks']),2) if (stats['internalLinks']>0 and stats['externalLinks']>0) else 0
                    stats['totLinks'] = stats['internalLinks'] + stats['externalLinks']
                    stats['rowToTableRatio'] = round(stats['rowCount']/float(stats['tableCount']),2) if (stats['rowCount']>0 and stats['tableCount']>0) else 0
                    
                    print(">>>" + siteurl +"<<<")
                    
                    features = '<webpage url="' + siteurl + '"'
                    for key, stat in stats.iteritems():
                        features += ' ' + key + '="'+ str(stat) +'"'
                    features += ' type="'+type + '" />'
                    
                    featurefile.write(features)
                    featurefile.flush()
                    
                    print(features)
                
                except Exception, err:
                    print(">>>>>>>>>>>" + url + "<<<<<<<<<<<<")
                    print(err)
                    continue
    
    #===========================================================================
    # checkMetaData
    # Given a BeautifulSoup object this method returns whether 'meta description' and 'meta keywords' 
    # are present in the object.
    # @param head: BeautifulSoup object 
    # @return: hasMetaDis, hasMetaKeywords, hasBlogWordInMetaData 
    #===========================================================================
    def checkMetaData(self, head):
        hasMetaDis = hasMetaKeywords = hasBlogWordInMetaData = hasForumWordInMetaData = False    
        description = head.find("meta", attrs={'name':re.compile("^description$", re.I)})
        keywords = head.find("meta", attrs={'name':re.compile("^keywords$", re.I)})
        if(description is not None):
            hasMetaDis = True
            hasBlogWordInMetaData = self.BLOG in description['content'].lower()
            hasForumWordInMetaData = self.FORUM in description['content'].lower()
#             print(description)
#             print(hasBlogWordInMetaData)
        if(keywords is not None):
            hasMetaKeywords = True
            hasBlogWordInMetaData = hasBlogWordInMetaData or self.BLOG in keywords['content'].lower()
            hasForumWordInMetaData = hasForumWordInMetaData or self.FORUM in keywords['content'].lower()
#             print(keywords)
#             print(hasBlogWordInMetaData)
        return hasMetaDis, hasMetaKeywords, hasBlogWordInMetaData, hasForumWordInMetaData            
       
#     def countImages(self, siteurl, page_images):
#         for x in range(0, len(page_images)):
#             page_images[x] = urlparse.urljoin(siteurl, page_images[x])
#         imgCount = len(page_images)
#         largeImgCount = ImageAnalyzer.countImages(page_images, self.IMAGE_THRESHOLD)
# #         print("Images: " +str(imgCount) + "Large Images: " + str(largeImgCount))
#         return imgCount, largeImgCount
    
    #===========================================================================
    # countImages
    # Counts the number of images (large images and total images) in a given url. This will first try to 
    # get the dimensions of a image using the html attributes in beautifulsoup object. If html attributes
    # are not present get the dimensions using the actual image.
    # @param siteurl: url for counting
    # @param images: a list of BeautifulSoup image objects 
    # @return: imgCount, largeImgCount
    #===========================================================================
    def countImages(self, siteurl, images):
#         print(images)
        imgCount = largeImgCount = 0
        page_images = list()
        for img in images:
            w = int(re.match(r'\d+', img.attrs['width']).group() if 'width' in img.attrs else -1)
            h = int(re.match(r'\d+', img.attrs['height']).group() if 'height' in img.attrs else -1)
#             print(str(w) )
            if(w > self.IMAGE_THRESHOLD or h > self.IMAGE_THRESHOLD):
                largeImgCount += 1
            elif(w < 0 or h < 0):
                page_images.append(urlparse.urljoin(siteurl, img['src']))
                
#         for x in range(0, len(page_images)):
#             page_images[x] = urlparse.urljoin(siteurl, page_images[x])
        imgCount = len(images)
        
        '''
        For images that do not have dimension attributes, try to get dimension by using the actuall image.
        '''
        largeImgCount += ImageAnalyzer.countImages(page_images, self.IMAGE_THRESHOLD)
#         print("Images: " +str(imgCount) + "Large Images: " + str(largeImgCount))
        return imgCount, largeImgCount
    
    #===========================================================================
    # checkURL
    # Returns if the word 'blog' is in the given url
    # @param siteurl: the url 
    # @return: Boolean
    #===========================================================================
    def checkURL(self, siteurl):
        return self.BLOG in siteurl, self.FORUM in siteurl
    
    #===========================================================================
    # checkTitle
    # Returns  if the word 'blog' is in the title of the webpage
    # @param soup: beautifulSoup object of the website 
    # @return: Boolean
    #===========================================================================
    def checkTitle(self, soup):
        tit = soup.find('title')
        if(tit is not None):
            return self.BLOG in tit.string.lower()
        return False
    
    #===========================================================================
    # CheckCommentsSection
    # Checks if the site has a comments section.
    # @param soup: beautifulSoup object of the website 
    # @return: Boolean
    #===========================================================================
    def CheckCommentsSection(self, soup):
        elem = soup.findAll(attrs={"id" : "comment*"}) + soup.findAll(attrs={"class" : re.compile('comment*')})
        return True if(len(elem) > 0) else False
    
    #===========================================================================
    # checkFeed
    # Returns if the site has feed links
    # @param head: beautifulSoup object of the website  
    # @return: Boolean
    #===========================================================================
    def checkFeed(self, head):
        for feed in head.findAll("link"):
            if feed.has_key('type') and (feed["type"] == "application/rss+xml" or feed["type"] == "application/atom+xml") and feed.has_key('href') and not "/comments/" in feed['href']:
                return True
        return False
    
    #===========================================================================
    # countLinks
    # Counts the number of internal/external links in a given website.
    # @param soup: beautifulSoup object of the website
    # @param siteurl: url of the web site 
    # @return: intLinks, extLinks
    #===========================================================================
    def countLinks(self, soup, siteurl):
        intLinks = extLinks = 0
        basedomain = urlparse.urlparse(siteurl)[1]
        for link in soup.findAll('a'):
            if(link.has_attr('href')):
#                 print(link['href'])
                fulllink = urlparse.urljoin(siteurl, link['href'])
                linkdomain = urlparse.urlparse(fulllink)[1]
                if(basedomain == linkdomain):
                    intLinks += 1
                else:
                    extLinks += 1
        return intLinks, extLinks
    
    def countTablesAndRows(self, soup):
        tables = soup.findAll('table')
        tr = soup.findAll('tr')
        return len(tables), len(tr)
    
    def countDiv(self, soup):
        return len(soup.findAll('div'))
    
    def countFrequentWords(self, soup):
        forumWords = orgWords = 0
        pagetext = soup.text.lower()
        
        for word in self.FORUM_FREQUENT_WORDS:
            forumWords += pagetext.count(word)
            
        for word in self.ORGANIZATION_FREQUENT_WORDS:
            orgWords += pagetext.count(word)
            
        return forumWords, orgWords
        