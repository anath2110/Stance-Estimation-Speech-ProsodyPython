# -*- coding: utf-8 -*-
"""
Created on Thur Dec 14 14:30:49 2017

@author: modified from Alonso's by Anindita Nath
University of Texas at ElPaso
"""


import numpy as np
import scipy
from prosodizeCorpus import prosodizeCorpus
from getfeaturespec import getfeaturespec
def concatenateFeatures(segInfo, exclude):
    nPatchesSoFar = 0   
    allpatcheslist=[]
    for i in range (len(segInfo)):
        if i == exclude:
            continue
        segment = segInfo[i]
        pfeatures = segment.features
        nPatchesInSegment = np.shape(pfeatures)[0]
        ncols = np.shape(pfeatures)[1]        
        allpatcheslist.append(pfeatures)
        nPatchesSoFar = nPatchesSoFar + nPatchesInSegment
   
    allpatchesarray=np.zeros((1,ncols))
    for i in range(len(allpatcheslist)):
        allpatchesarray=np.vstack((allpatchesarray,allpatcheslist[i]))
        
    allpatchesarray=np.delete(allpatchesarray,0,axis=0)   
    return allpatchesarray

#segData= prosodizeCorpus('stance-master/testeng/audio/', 'stance-master/testeng/annotations/', getfeaturespec('stance-master/src/mono4.fss'), 100)
#
#allpatches=concatenateFeatures(segData,-1)
#scipy.io.savemat('concanpy.mat', {'concanpy': allpatches})
#means = np.mean(allpatches,axis=0)
#stddevs = np.std(allpatches,axis=0)
#print(means.shape)
#print(stddevs.shape)
