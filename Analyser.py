from __future__ import division
from StatXMLReader import readMetaDataXML
from StatXMLReader import readMetaAnalyseXML
from xml.etree.cElementTree import ElementTree
descount=0
keywcount=0
both = 0
root = readMetaDataXML("BlahBlah")
rootAnalyse = readMetaAnalyseXML("BlahBlah")
tot = len(root)
print">>Total Pages: " + str(tot)
for child in root:
    des = child.get('description')
    key = child.get('keywords')
    if(len(des)>0 and len(key) == 0):
        descount += 1
    if(len(key)>0 and len(des) == 0):
        keywcount += 1
    if(len(des)>0 and len(key)>0):
        both += 1

nometa = tot - (descount + keywcount + both)
print">>Pages with meta description: " + str(descount) + " (" + str(int(round(descount*100/tot))) + "%)"
print">>Pages with meta keywords: " + str(keywcount) + " (" + str(int(round(keywcount*100/tot))) + "%)"
print">>Pages with both: " + str(both) + " (" + str(int(round(both*100/tot))) + "%)"
print">>Pages with no metadata: " + str(nometa) + " (" + str(int(round(nometa*100/tot))) + "%)"

totNode  = rootAnalyse.find('pages')
desNode = rootAnalyse.find('description')
keyNode = rootAnalyse.find('keywords')
bothNode = rootAnalyse.find('both')
noneNode = rootAnalyse.find('none')

totNode.text = str(tot)
desNode.text = str( descount)
keyNode.text = str(keywcount)
bothNode.text = str(both)
noneNode.text = str(nometa)

Doc=ElementTree(rootAnalyse) 
Doc.write('output/data/meta_analyse.xml')