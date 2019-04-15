#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 09:44:42 2019

@author: polo
"""
from LoadXML import LoadXML_to_Sessions

from nltk.tag.stanford import StanfordNERTagger
from nltk.tokenize import word_tokenize

tagger = StanfordNERTagger('/home/polo/Downloads/stanford-ner-2018-02-27/classifiers/english.all.3class.distsim.crf.ser.gz',
                           '/home/polo/Downloads/stanford-ner-2018-02-27/stanford-ner.jar', encoding='utf-8')

def formatted_entities(classified_paragraphs_list):
    entities = {'persons': list(), 'organizations': list(), 'locations': list()}
               # 'Money': list(), 'Percent': list(), 'Date': list(),'Time': list()}

    for classified_paragraph in classified_paragraphs_list:
        for entry in classified_paragraph:
            entry_value = entry[0]
            entry_type = entry[1]

            if entry_type == 'PERSON':
                entities['persons'].append(entry_value)

            elif entry_type == 'ORGANIZATION':
                entities['organizations'].append(entry_value)

            elif entry_type == 'LOCATION':
                entities['locations'].append(entry_value)
                
    return entities

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

Sessions,Queries = LoadXML_to_Sessions()

tokenized_Queries = []

for Query in Queries:
    tokenized_Queries.append(word_tokenize(Query))
    
classified_Text_list = tagger.tag_sents(tokenized_Queries)

NER = NER_Entities(classified_Text_list,Queries)


    
#formatted_result = formatted_entities(classified_Text_list)

