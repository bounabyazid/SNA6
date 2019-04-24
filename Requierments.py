#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 10:33:07 2019

@author: polo
"""
import numpy as np
from scipy import mean

import community
import networkx as nx

import matplotlib.pyplot as plt

#https://github.com/taynaud/python-louvain/

G = nx.gnp_random_graph(50, 0.5, directed=False)
nx.draw(G, node_size=50, labels=None, with_labels=True)
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

def Degree_Distribution(G,plot=False):
    degree_hist = nx.degree_histogram(G) 
    degree_hist = np.array(degree_hist, dtype=float)
    degree_prob = degree_hist/G.number_of_nodes()
    
    if plot:
       plt.plot(degree_hist,degree_prob,'b.')
       plt.loglog(degree_hist,degree_prob)
    
       plt.xlabel('degree')
       plt.ylabel('p(degree)')
       plt.title('Degree Distribution')
    
       plt.hist(degree_hist)
       plt.show()
    
    return degree_prob

def graph_global_measures(G):
    mean_DD = round(mean(Degree_Distribution(G),plot=False),2)
    GCoeff = round(nx.transitivity(G),2)
    mean_path_len = round(nx.average_shortest_path_length(G),2)
    diameter = nx.diameter(G)
    return mean_DD, GCoeff, mean_path_len, diameter
    
def node_rank(G):
    Node_Rank = {'Degree distribution':'','Betweenness Centrality':'','Average path length':''}
    degree_prob = Degree_Distribution(G,plot=False)
    Node_Rank['Degree distribution'] = int(np.argmax(degree_prob))
    
    bw_centrality = nx.betweenness_centrality(G, normalized=True)
    #So, If You want to get the values less than 1, You have to use normalized=True

    for k, v in bw_centrality.items():
        bw_centrality[k] = round(v, 2)
        
    #print ("Betweenness Centrality:",bw_centrality)
    
    Node_Rank['Betweenness Centrality'] = max(bw_centrality, key=bw_centrality.get)
    
    mean_shortest_paths = {}
    for source in range(G.number_of_nodes()):
        #paths_len = []
        #for target in range(G.number_of_nodes()):
            #if source != target:
               #shortest_simple_paths(G, source, target, weight=None)
            #   paths_len.append(nx.shortest_path_length(G,source,target))
        #mean_shortest_paths[source] = paths_len

        mean_shortest_paths[source] = mean(list(nx.shortest_path_length(G,source).values))
    Node_Rank['Average path length'] = min(mean_shortest_paths, key=mean_shortest_paths.get)
    
    return Node_Rank, mean_shortest_paths

def Community_detection(G):
    #http://ryancompton.net/2014/06/16/community-detection-and-colored-plotting-in-networkx/
    parts = community.best_partition(G)
    values = [parts.get(node) for node in G.nodes()]

    nx.draw_spring(G, cmap = plt.get_cmap('jet'), node_color = values, node_size=220, with_labels=True)

    print ('we have ',len(list(set(values))),' Communities')
    
    Communities = []
    for val in list(set(values)):
        Communities.append(G.subgraph([k for k,v in parts.items() if v == val]))
    
    return parts, Communities
    

def Small_World():
    watts_strogatz = nx.watts_strogatz_graph(20,2,0.15)
    nx.nodes(watts_strogatz)

    EG= nx.erdos_renyi_graph(50,0.5)

parts, Communities = Community_detection(G)
Node_Rank, mean_shortest_paths = node_rank(G)
degree_prob = list(Degree_Distribution(G,plot=False))