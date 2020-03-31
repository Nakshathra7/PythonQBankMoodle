import xml.etree.ElementTree as ET
import time
from xml.dom import minidom
from xml.dom.minidom import parseString

import lxml.etree as le

#path = 'questions-IA510.xml'
path = 'testQuestions-IA510.xml'

tree = ET.parse(path)
doc = le.parse(path)

root = tree.getroot()
prev = None

file = open('testQuestions-IA510.xml','r')
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

i = len(dom.getElementsByTagName('question'))
questionCount = 0
questionDict = {}
questionTag = []
questionTextDict = {}
questionTextCount = 0
questionTextValuesDict = {}
questionTextTag = []
questionTextValuesDictForRemoval = {}
questionTextValues = []
questionDictAfterRemoval = {}
nonDuplKeys = []
count = None
questionForRemoval = []

for node in doc.iter('quiz'):
#for node in tree.iter('quiz'):
    elems_to_remove = {}
    for elem in node.iter():
        #If loop to get Question tag values and storing the same in Dictionary and List
        if str(elem.tag)=='question' and elem.find('questiontext'):       
            questionCount = questionCount + 1
            questionDict[questionCount] = elem
            questionTag.append(elem)
            continue
        #If loop to get QuestionText tag values and storing the same in Dictionary and List
        if str(elem.tag)=='questiontext':
            elemText = elem.find('text')
            questionTextCount = questionTextCount + 1
            questionTextDict[questionTextCount] = elem
            questionTextTag.append(elem)
            questionTextValues.append(elemText)
            questionTextValuesDict[questionTextCount] = elemText
            parent=elem.getparent()
            print("parent",parent)
            continue

#Loop to identify duplicate questions by comparing text and extracting questions for removal
for i in range(0, len(questionTextValues)-1):
   if (questionTextValues[i]).text == (questionTextValues[i+1]).text:
        elems_to_remove[i] = questionTextValues[i]
        questionTextValuesDictForRemoval[i] = questionTag[i]
        questionForRemoval.append(questionTextValuesDictForRemoval.values())

'''
#Loop to fetch Non Duplicate Question Keys
for key in questionDict.keys(): 
    if not key in elems_to_remove: 
        nonDuplKeys.append(key)

#Loop to compare and fetch Non Duplicate Question tag values
for list_item in nonDuplKeys: 
    for dict_key in questionDict.keys():
        if list_item == dict_key:
            questionDictAfterRemoval[list_item] = questionDict.values()            
'''

print("questionDict",len(questionDict))
print("questionTextDict",len(questionTextDict))
print("elems_to_remove",len(elems_to_remove))
print("questionForRemoval",len(questionForRemoval))
print(len(nonDuplKeys))

#Loop to get questiontext elementtree and compare for duplicates. This is old method not used in this file for comparing
for question in root.iter('questiontext'):                     
    elems_to_remove = []
    for questionsText in question:
        questions = questionsText.text
        if elements_equal(questionsText, prev):
            elems_to_remove.append(questionsText)
            continue
        prev = questionsText
    
    #Loop to remove duplicate question from xml element tree. This will accept only element tree format, and not Dict or List.
    for elem_to_remove in elems_to_remove:
        question.remove(elem_to_remove)

doc .write("out.xml")
