#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 09:12:08 2019

@author: Yazid Bounab
"""

import pandas as pd 
from SNA_NER import NER_Spacy2
from nltk import pos_tag, word_tokenize
from LoadXML import LoadXML_to_Sessions

text = 'Google is a friend of Facebook and Yahoo shouts at Microsoft because Stackoverflow is giving out hats.'
text='amazon'
text='nurses sue douglas kennedy'

def POSofQueries():
    QPOS=[]
    QPERS = []
    QORG = []
    QLOC = []
    
    Sessions,Queries = LoadXML_to_Sessions()
    for query in Queries:
        POS=[]
        for word, pos in pos_tag(word_tokenize(query)):
            POS.append ({word: pos})
        QPOS.append(POS)
        
        PERS, ORG, LOC = NER_Spacy2(query)
        
        QPERS.append(PERS)
        QORG.append(ORG)
        QLOC.append(LOC)
        
    return pd.DataFrame({'Query': Queries,'POS':QPOS, 'Personnes':QPERS,'Organisations':QORG,'Locations':QLOC})

df = POSofQueries()
