# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 09:33:05 2019

@author: Yazid and Karol

"""
from scipy import mean

def Histogramme(Dict):
    avrg = 0
    avrg = int(mean(list(Dict.values())))
    return Dict[str(avrg)]
    
def AdjancancyMatrix():
    return True
    
def createGraph():
    return True
    
Dict = {'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8}
#Dict = [1,2,3,4,5,6,7,8]
print (Histogramme(Dict))
