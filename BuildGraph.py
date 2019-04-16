#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 12:23:04 2019

@author: Yazid and Karol
"""

import numpy as np
import editdistance as ED

from scipy import mean
from SNA_NER import NER_Stanford

#Dict = {'1':7,'2':5,'3':5,'4':4,'5':8,'6':3,'7':7,'8':8}

def Histogramme(Dict):
    avrg = int(mean(list(Dict.values())))
    print (avrg)
    myList = [abs(val-avrg) for val in Dict.values()]
    Closest = myList.index(min(myList))
    print (list(Dict.keys())[Closest])
    return Dict[str(list(Dict.keys())[Closest])]

def Similarity_EditDistance(S1,S2):
    Sum1 = 0
    for q1 in S1:
        Sum = 0
        for q2 in S2:
            Sum += ED.eval(q1, q2)
        Sum1 += Sum/len(S2)
    
    Sum2 = 0
    for q2 in S2:
        Sum = 0
        for q1 in S1:
            Sum += ED.eval(q2, q1)
        Sum2 += Sum/len(S1)    
    #return round((Sum1+Sum2)/2, 2)
    return int((Sum1+Sum2)/2)


def AdjancancyMatrix():
    NER = NER_Stanford()
    QNER = []
    Dict = {}
    
    for Q in NER:
        for key in Q:
            QNER.append(Q[key])
            
    relatedness = np.zeros( (len(NER), len(NER)) )
    
    for i in range (0,len(QNER)-1):
        for j in range (1,len(QNER)):
            relatedness[i][j] = Similarity_EditDistance(QNER[i],QNER[j])
    
    for val in set(relatedness.flatten()):
        Dict[str(val)] = list(relatedness.flatten()).count(val)
    Threshold = Histogramme(Dict)
    
    return NER,QNER,relatedness,Dict,Threshold
    
def createGraph():
    return True
    
NER,QNER,relatedness,Dict,Threshold = AdjancancyMatrix()