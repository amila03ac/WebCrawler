'''
Created on Feb 1, 2013

@author: Anghiari
'''
import sys
from WebCrawler import crawlLinks
import logging
import time

url = sys.argv[1]
limit = int(sys.argv[2])
crawled = set([])
logging.basicConfig(filename='log/activity.log',level=logging.INFO)
with open('log/activity.log', 'w'):
	pass

localtime = time.asctime( time.localtime(time.time()) )
logging.info(localtime)
logging.info("--------------------------------------------")

if(crawlLinks(url, limit)):
	print "Successfully Completed"
	logging.info("Successfully Completed")
else:
	print "Failed"
	logging.info("Failed")




