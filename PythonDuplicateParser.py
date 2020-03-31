import xml.etree.ElementTree as ET
import time
from xml.dom import minidom
from xml.dom.minidom import parseString

import lxml.etree as le

path = 'questions-IA510.xml'
#path = 'out.xml'

tree = ET.parse(path)
doc = le.parse(path)        #Library to fetch parent node

root = doc.getroot()
prev = None

file = open('questions-IA510.xml','r')
data = file.read()
file.close()
dom = parseString(data)


def elements_equal(e1, e2):
    if type(e1) != type(e2):
        return False
    #if e1.tag != e2.tag: return False
    if e1.text != e2.text: return False
    #if e1.tail != e2.tail: return False
    #if e1.attrib != e2.attrib: return False
    if len(e1) != len(e2): return False
    return all([elements_equal(c1, c2) for c1, c2 in zip(e1, e2)])

#Loop to get question tag elementtree
for question in doc.iter('question'):                     
    elems_to_remove = []
    #Loop to get questiontext tag elementtree
    for questionsText in question.iter('questiontext'):
        if elements_equal(questionsText, prev):
            #Fetching parent question tag for the identified questiontext duplicates
            parentQuestion = questionsText.getparent()
            elems_to_remove.append(parentQuestion)
            #print("elems_to_remove",(elems_to_remove))
            continue
        prev = questionsText

    for elem_to_remove in elems_to_remove:
        root.remove(elem_to_remove)

doc.write("out.xml")


