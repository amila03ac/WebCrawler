'''
Created on Jan 31, 2013

@author: Anghiari
'''

import os



def makeDirectory(pageName):    
    directory="./"+pageName
    print(directory)

    if not os.path.exists(directory):
        os.mkdir(directory)
            
 
        
def saveAsHtmlPage(pageName,title,content):

    directory="./"+pageName
    print(directory)

    if not os.path.exists(directory):
        os.mkdir(directory)
        
    f=open("./"+pageName+"/"+title+".xml", "wb")
    f.write(content)
    f.close()
            
            
            
        
        
       
    
    
    

    

    
    
    