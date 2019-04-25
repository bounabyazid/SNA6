#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 12:23:04 2019

@author: Yazid and Karol
"""
import collections
import numpy as np
import editdistance as ED

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

from scipy import mean
from SNA_NER import NER_Stanford

import matplotlib.pyplot as plt
import networkx as nx

from Requierments import Degree_Distribution, Small_World, Community_detection, Graph_Global_Mesures

#Dict = {'1':7,'2':5,'3':5,'4':4,'5':8,'6':3,'7':7,'8':8}

def Histogramme(Dict):
    avrg = int(mean(list(Dict.values())))
    #print (avrg)
    myList = [abs(val-avrg) for val in Dict.values()]
    Closest = myList.index(min(myList))
    print ('Threshold',list(Dict.keys())[Closest])
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

def Topics_Words(lda_model,num_words):
    Topic_Words = []
    #for index, topic in lda_model.show_topics(formatted=False, num_words= 30):
        #print('Topic: {} \nWords: {}'.format(index, [w[0] for w in topic]))
    for index, topic in lda_model.show_topics(formatted=False, num_words= num_words):
        Topic_Words.append([w[0] for w in topic]) 
    return Topic_Words

def LDA_Query_Communitiies(NER,QNER,Communities_Nodes):
    Query_Comunities = {}

    for community in Communities_Nodes:
        docs = []
        
        for node in Communities_Nodes[community]:
            docs.append(QNER[node])
            
        # Create Dictionary
        id2word = corpora.Dictionary(docs)

        # Create Corpus
        texts = docs

        # Term Document Frequency
        corpus = [id2word.doc2bow(text) for text in texts]
    
        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=5, 
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                alpha='auto',
                                                per_word_topics=True)
        
        Query_Comunities[community] = Topics_Words(lda_model,num_words=5)
    
    return Query_Comunities
    
#NER,QNER,relatedness,Dict,Threshold,M = AdjancancyMatrix()

#G = createGraph(M,NER)

#Degree_Distribution(G,plot=True)

#Communities, Communities_Nodes = Community_detection(G)

#Query_Comunities = LDA_Query_Communitiies(NER,QNER,Communities_Nodes)

#Small_World(len(NER),G)
F = open('Config.txt','w') 

for k in range(20,157):
    for p in np.arange(0.1, 0.9, 0.05):
        watts_strogatz = nx.watts_strogatz_graph(158,k,p)
        nx.nodes(watts_strogatz)
        mean_DD3, GCoeff3, mean_path_len3, diameter3 = Graph_Global_Mesures(watts_strogatz)
        S = 'k='+str(k)+' p='+str(p)+' Mean='+str(mean_DD3)+' CC='+str(GCoeff3)+' avg_path='+str(mean_path_len3)+' Diameter='+str(diameter3)
        F.write(S)
        
F.close()