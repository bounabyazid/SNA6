#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 10:33:07 2019

@author: polo
"""

import matplotlib.pyplot as plt
import networkx as nx

from scipy import mean
import numpy as np

G = nx.gnp_random_graph(10, 0.5, directed=True)
nx.draw(G, node_size=10, labels=None, with_labels=True)
A = nx.adjacency_matrix(G).todense()
plt.show()

    
def plot_degree_dist(G):
    all_degrees = [G.degree(n) for n in G.nodes()]
    degrees = list(set(all_degrees))
    #Degree_Dist = [all_degrees.count(degree)/G.number_of_nodes() for degree in degrees]
    Degree_Dist = [all_degrees.count(n)/G.number_of_nodes() for n in range(G.number_of_nodes())]
    
    print (round(sum(Degree_Dist),2),round(mean(list(Degree_Dist)),2))
    
    plt.plot([i for i in range(0,G.number_of_nodes())], [np.log10(DDist) for DDist in Degree_Dist]) 
    
    #plt.loglog(degrees, Degree_Dist)
    plt.xlabel('degree')
    plt.ylabel('p(degree)')
    plt.title('Degree Distribution')
    
    #plt.hist(Degree_Dist)
    plt.show()
    
    return degrees,Degree_Dist

def Degree_Distribution(G):
    degrees = [G.degree(n) for n in G.nodes()]

    #Degree_Dist = [all_degrees.count(degree)/G.number_of_nodes() for degree in degrees]
    Degree_Dist = [float(degrees.count(n)/G.number_of_nodes()) for n in range(1,G.number_of_nodes()+1)]
        
    plt.plot([i for i in range(1,len(Degree_Dist)+1)], [np.log10(DDist) for DDist in Degree_Dist]) 
    #plt.plot([i for i in range(0,len(Degree_Dist))], Degree_Dist) 


    #plt.loglog(degrees, Degree_Dist)
    plt.xlabel('degree')
    plt.ylabel('p(degree)')
    plt.title('Degree Distribution')
    
    #plt.hist(Degree_Dist)
    plt.show()
    
    return degrees,Degree_Dist

def DDistNX(G):
    degrees = {}
    for n in range(1,G.number_of_nodes()+1):        
        degrees[n]=G.degree(n)
    
    values= sorted(set(degrees.values()))
    hist= [list(degrees.values()).count(x) for x in values]
    
    return degrees,hist

degrees,hist = DDistNX(G)
#degrees,Degree_Dist = Degree_Distribution(G)

def plot_degree_distribution (wiki):
    degs = {}
    for n in wiki.nodes():
        deg = wiki.degree(n)
        if deg  not in degs:
           degs[deg] = 0
        degs[deg] += 1
    items = sorted(degs.items ())
    fig = plt.figure ()
    ax = fig.add_subplot (111)
    ax.plot([k for (k,v) in items], [v for (k,v) in  items ])
    ax.set_xscale('log')
    #ax.set_yscale('log')
    plt.title("Wikipedia  Degree  Distribution")
        #fig.savefig("degree_distribution.png")
        
#plot_degree_distribution (G)

def plot_degree_dist(G):
    degree_hist = nx.degree_histogram(G) 
    degree_hist = np.array(degree_hist, dtype=float)
    degree_prob = degree_hist/G.number_of_nodes()
    plt.loglog(np.arange(degree_prob.shape[0]),degree_prob,'b.')
    plt.xlabel('k')
    plt.ylabel('p(k)')
    plt.title('Degree Distribution')
    plt.show()
    
#plot_degree_dist(G)
    
    #degree_hist = nx.degree_histogram(G) 
    #degree_hist = np.array(degree_hist, dtype=float)
    #degree_prob = degree_hist/G.number_of_nodes()