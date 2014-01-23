'''
Created on Apr 27, 2013

@author: Anghiari
'''

import xml.etree.ElementTree as ET


def readXMLFile(filepath):
    
    tree = ET.parse(filepath)
    root = tree.getroot()

    return root

def readXML(filepath):
    
    tree = ET.parse('output/data/stats.xml')
    root = tree.getroot()

    return root

def readImgXML(filepath):
    tree = ET.parse('output/data/imgStats.xml')
    root = tree.getroot()

    return root

def readMetaXML(filepath):
    tree = ET.parse('output/data/meta.xml')
    root = tree.getroot()

    return root

def readMetaDataXML(filepath):
    tree = ET.parse('output/data/meta_data_raw.xml')
    root = tree.getroot()

    return root

def readMetaAnalyseXML(filepath):
    tree = ET.parse('output/data/meta_analyse.xml')
    root = tree.getroot()

    return root
    
#    details=info[0]
#    elements=info[1]
#    i=0
#    
#    for element in elements:
#        i=0
#        for stat in stats:
#            
#            if(stat==element[0]):
#                
#                element[1].set(element[1]+values[i])
#                break
#            
#            i+=1
#    
#    tree.write('big.xml')


    

            
    
            
            
            
            
            
            
            
            