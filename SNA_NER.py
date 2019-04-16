#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 09:44:42 2019

@author: polo
"""
from LoadXML import LoadXML_to_Sessions

from nltk.tag.stanford import StanfordNERTagger
from nltk.tokenize import word_tokenize

import pprint
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()


#tagger = StanfordNERTagger('/home/polo/Downloads/stanford-ner-2018-02-27/classifiers/english.all.3class.distsim.crf.ser.gz',
#                           '/home/polo/Downloads/stanford-ner-2018-02-27/stanford-ner.jar', encoding='utf-8')

def NER_Entities(classified_Text_list,Queries):
    NER = []
    NE = ['PERSON', 'ORGANIZATION', 'LOCATION']

    for i in range(0,len(classified_Text_list)):   
        L = []
        for entry in classified_Text_list[i]:
            entry_value = entry[0]
            entry_type = entry[1]

            if entry_type in NE:
               L.append(entry_value)

        NER.append({Queries[i]:L})
        
    return NER

def NER_Stanford():
    Sessions,Queries = LoadXML_to_Sessions()

    tokenized_Queries = []

    for Query in Queries:
        tokenized_Queries.append(word_tokenize(Query))
    
    classified_Text_list = ''#tagger.tag_sents(tokenized_Queries)

    NER = NER_Entities(classified_Text_list,Queries)
    return NER

def NER_Spacy():
    'https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da'
    NER = []
    Sessions,Queries = LoadXML_to_Sessions()
    for Query in Queries:
        doc = nlp(Query)
        NER.append({Query:[(X.text, X.label_) for X in doc.ents]})
    return NER
    
def NER_Spacy2(Query):
    QPERS = []
    QORG = []
    QLOC = []
    
    doc = nlp(Query)
    for entity in doc.ents:
        if entity.label_ == 'PERSON':
           QPERS.append(entity.text)
        elif entity.label_ == 'ORG':
            QORG.append(entity.text)
        elif entity.label_ == 'LOC':
            QLOC.append(entity.text)
            
    return QPERS, QORG, QLOC
