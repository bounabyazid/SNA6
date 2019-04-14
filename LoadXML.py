#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 08:41:28 2019
@author: Yazid Bounab
"""
import pandas as pd 
import xml.etree.ElementTree as et 

xtree = et.parse("Webscope_L24/ydata-search-query-log-to-entities-v1_0.xml")
xroot = xtree.getroot()

Sessions = []

IDS = []
Queries = []

children = xroot.getchildren()
for child in children:
    Session = {'id':'','numqueries':'','queries':[]}
    
    Session['id'] = child.attrib.get("id")
    Session['numqueries'] = child.attrib.get("numqueries")
    
    IDS.append(Session['id'])
    
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
    
IDS = list(set(IDS))
Queries = list(set(Queries))
