# -*- coding: utf-8 -*-
"""
Created on Thur Dec 14 14:30:49 2017
modified on Wed 02.22.2018
@author: modified from Alonso's by Anindita Nath
University of Texas at ElPaso
"""


import numpy as np
import scipy
import time
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
        if(pfeatures.size!=0):
            nPatchesInSegment = np.shape(pfeatures)[0]
            #print(nPatchesInSegment)        
            ncols = np.shape(pfeatures)[1] 
            #print(ncols)
            allpatcheslist.append(pfeatures)
            nPatchesSoFar = nPatchesSoFar + nPatchesInSegment
   
    allpatchesarray=np.zeros((1,ncols))
    for i in range(len(allpatcheslist)):
        allpatchesarray=np.vstack((allpatchesarray,allpatcheslist[i]))
        
    allpatchesarray=np.delete(allpatchesarray,0,axis=0)   
   
    return allpatchesarray
#
#start=time.time()
#segData= prosodizeCorpus('../testeng/audio/', '../testeng/annotations/', getfeaturespec('../testeng/featurefile/mono4.fss'), 100,lang='E')
#
#allpatches=concatenateFeatures(segData,-1)
#print(allpatches.shape)
#end=time.time()
#print(end-start)

#scipy.io.savemat('concanpy.mat', {'concanpy': allpatches})
#means = np.mean(allpatches,axis=0)
#stddevs = np.std(allpatches,axis=0)
#print(means.shape)
#print(stddevs.shape)
