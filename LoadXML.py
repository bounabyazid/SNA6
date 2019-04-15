#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 08:41:28 2019
https://robertopreste.com/blog/parse-xml-into-dataframe
@author: Yazid BOUNAB
"""
import pickle

import pandas as pd 
import xml.etree.ElementTree as et 


def SaveListToFile(mylist,filename):
    with open(filename, 'wb') as filehandle:
         pickle.dump(mylist, filehandle)
         
def LoadFileToList(filename):
    mylist = []
    with open(filename, 'rb') as filehandle:  
         mylist = pickle.load(filehandle)
    return mylist

def LoadXML_to_Sessions():
    xtree = et.parse("Webscope_L24/ydata-search-query-log-to-entities-v1_0.xml")
    xroot = xtree.getroot()

    Sessions = []
    #for child in xroot:
    Queries = []
    children = xroot.getchildren()
    for child in children:
        Session = {'id':'','numqueries':'','queries':[]}
    
        Session['id'] = child.attrib.get("id")
        Session['numqueries'] = child.attrib.get("numqueries")
    
        #Session['query'] = child[0].find('text').text
        #print (et.dump(child))
        for node in child:
            Attributes = {'adult':'', 'ambiguous':'', 'assessor':'', 'cannot-judge':'', 'navigational':'', 'no-wp':'', 'non-english':'', 'quote-question':'', 'starttime':''}
            Query = {'text':'','attribues':Attributes,'annotations':[]}
            Query['text'] = node.find('text').text if node is not None else None
        
            Queries.append(Query['text'])
        
            for key in Attributes.keys():
                Query['attribues'][key] = node.attrib.get(key)
            
            for annot in node.findall('annotation'):
                annotation = {'main':'','span':''}
                annotation['main'] = annot.attrib.get("main")
                annotation['span'] = annot.find('span').text
            
                if annot.find('target'):
                   Target = {'wiki-id':'','link':''}
                   Target['id'] = annot.find('target').attrib.get('wiki-id')
                   Target['link'] = annot.find('target').text
               
                   annotation['target'] = Target
                Query['annotations'].append(annotation)
        
            Session['queries'].append(Query)
        Sessions.append (Session)
    return Sessions,Queries

#Sessions,Queries = LoadXML_to_Sessions()

#SaveListToFile(Queries,'Data/Queries.pkl')
#SaveListToFile(Sessions,'Data/Sessions.pkl')
