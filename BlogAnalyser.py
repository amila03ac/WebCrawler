import re
from bs4 import BeautifulSoup, Comment

KEYWORDS = ['latest', 'archive', 'posts', 'recent', 'articles']

#===============================================================================
# countParaAndWord
# Given a BeautifulSoup object of a web page this method counts the number of paragraphs, words,
# and small paragraphs (paragraphs with 5<words<25).
# @param soup: BeautifulSoup object
# @return: paraCount 
# @return: smallParaCount 
# @return: wordCount
#===============================================================================
def countParaAndWord(soup):
   
    parents = ['div', 'p', 'td', 'tr', 'li', 'dd']
    badguys = ['a', 'i', 'span', 'b', 'strong', 'em']
    
    for tag in badguys:
        for a in soup.findAll(tag):
            if(a.parent is not None and a.parent.name in parents and a.string is not None):
    #             print(">>ME DAD: " + str(a.parent))
    #             print(">>ME SIS: " + str(a.previousSibling))
    #             print(">>MEEEEE: " + str(a))
    #             print(">>ME BRO: " + str(a.nextSibling))
    #             
                p = ''
                n = ''
                prev = a.previousSibling
                nxt = a.nextSibling
                
                prevOK = prev is not None and not hasattr(prev, 'name')
                nxtOK = nxt is not None and not hasattr(nxt, 'name')
                
                if(prevOK and nxtOK):
    #                 print(">>>>>>>>PrevOK and NxtOK<<<<<<<<<<<<")
                    p = prev
                    n = nxt
                    prev.replaceWith(p + a.string + n)
                    nxt.extract()
                    a.extract()
                elif(prevOK):
    #                 print(">>>>>>>>>>PrevOK<<<<<<<<<<")
                    p = prev
                    prev.replaceWith(p + a.string + n)
                    a.extract()
                elif(nxtOK):
    #                 print(">>>>>>>>>>NxtOK<<<<<<<<<<")
                    n = nxt
                    a.replaceWith(p + a.string + n) 
                    nxt.extract()
                else:
    #                 print(">>>>>>>>>PrevNOTOK and NxtNOTOK<<<<<<<<<<")
                    a.replaceWith(p + a.string + n)
                    
    #             print('-----------------------------------------')
    
    paraCount = 0
    smallParaCount = 0
    wordCount = 0
    for txt in soup.findAll(text=True):
        if(not txt.isspace()):
            s = unicode(txt).encode('utf8')
#             print(s)
            splt = txt.split()
            wordCount += len(splt)
            if(len(splt) > 25):
                paraCount += 1
            elif(len(splt) > 5):
                smallParaCount += 1
#                 print(">>>This is the " +str(paraCount)+" Paragraph Baby :D")
#             print("---------------------------------------------------------")
    
#     print("Number of Paragraphs: " + str(paraCount))
#     print("Number of Small Paragraphs: " + str(smallParaCount))
#     print("Number of Words: " + str(wordCount))
    
    return paraCount, smallParaCount, wordCount

#===============================================================================
# checkForArchiveList
# Finds if a web page has an archive list of links. (ex: popular posts, recent posts)
# @param soup: BeautifulSoup object
# @return: True if archive exists, else False
#===============================================================================

def checkForArchiveList(soup):
    for tag in soup.findAll(re.compile(r"^(h1|h2|h3)$")):
        text = tag.text.lower()
        for keyword in KEYWORDS:
            if(keyword in text):
                return True
    return False