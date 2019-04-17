#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 12:23:04 2019

@author: Yazid and Karol
"""
import collections
import numpy as np
import editdistance as ED

from scipy import mean
from SNA_NER import NER_Stanford

import matplotlib.pyplot as plt
import networkx as nx

#Dict = {'1':7,'2':5,'3':5,'4':4,'5':8,'6':3,'7':7,'8':8}

def Histogramme(Dict):
    avrg = int(mean(list(Dict.values())))
    print (avrg)
    myList = [abs(val-avrg) for val in Dict.values()]
    Closest = myList.index(min(myList))
    print (list(Dict.keys())[Closest])
    #return Dict[str(list(Dict.keys())[Closest])]
    return list(Dict.keys())[Closest]

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
        Dict[val] = list(relatedness.flatten()).count(val)
    Threshold = Histogramme(Dict)
    
    M = np.zeros( (len(NER), len(NER)) )
    
    for i in range (0,len(QNER)-1):
        for j in range (1,len(QNER)):
            if relatedness[i][j] >= Threshold:
               M[i][j] = 1
    
    return NER,QNER,relatedness,Dict,Threshold,M

def createGraph(M,NER_Queries):
    Nodes = []
    for D in NER_Queries:
        Nodes.extend(D.keys())
    #Nodes = list(np.arange(1,len(D.keys())))
    
    rows, cols = np.where(M == 1)
    edges = zip(rows.tolist(), cols.tolist())
    G = nx.Graph()
    G.add_edges_from(edges)
    nx.draw(G, node_size=len(Nodes), labels=None, with_labels=True)
    
    plt.show()
    
    return G

def Degree_Histogram(G):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
    # print "Degree sequence", degree_sequence
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())

    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.80, color='b')

    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)

    # draw graph in inset
    #plt.axes([0.4, 0.4, 0.5, 0.5])
    #Gcc = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)[0]
    #pos = nx.spring_layout(G)
    #plt.axis('off')
    #nx.draw_networkx_nodes(G, pos, node_size=20)
    #nx.draw_networkx_edges(G, pos, alpha=0.4)

    plt.show()
    
    return deg, cnt,degree_sequence

def Graph_Global_Mesures(G):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
    # print "Degree sequence", degree_sequence
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    degdist = []
    
    for i in range(0,len(cnt)):
        degdist.append(cnt[i]/len(cnt))
        
    return deg, cnt,degree_sequence,degdist
    
NER,QNER,relatedness,Dict,Threshold,M = AdjancancyMatrix()

G = createGraph(M,NER)

deg, cnt,degree_sequence, degdist = Graph_Global_Mesures(G)