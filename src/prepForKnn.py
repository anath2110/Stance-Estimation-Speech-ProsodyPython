# -*- coding: utf-8 -*-
"""
Created on Thur Dec 14 21:30:49 2017

@author: modified from Alonso's by Anindita Nath
University of Texas at ElPaso
"""

import numpy as np
import scipy
import numpy.matlib
from concatenateFeatures import concatenateFeatures
from makePPM import makePPM
def prepForKnn(segData,exclude,showStats):
    # create two parallel matrices, of features and target values
    # for the first: concatenate all segments' patches then add temporals
    # for the second: repmat and conatenate properties for each segment
    # exclude is the number of a segment to exclude, if any (for leave-one-out testing)
    # similar to Jason's buildRegTrainingData
    # converted from original by Nigel Ward and Ivan Gris, UTEP, June 2017
    # see ../doc/UTEP-prosody-overview.docx
  
       
    
  
  featuresForAllPatches = concatenateFeatures(segData, exclude)
  nPatchesSoFar = 0
  propsForAllPatches = np.zeros((1,len(segData[0].properties)))
 
 
  for i in range (len(segData)):
    if i==exclude:
      #print('prepexclde')
      continue
    #if (len(nullindex)==0 and i in nullindex):
        #print("prepforKnn")
        #print(i)
        #continue
    segment = segData[i]
    pfeatures = segment.features  
    if(pfeatures.size!=0):
        nPatchesInSegment = np.shape(pfeatures)[0]  
        #print(segment.features.shape)
        repeatedProperties = np.matlib.repmat(segment.properties, nPatchesInSegment, 1)
        #print(repeatedProperties.shape)
        propsForAllPatches = np.vstack((propsForAllPatches,repeatedProperties))
        nPatchesSoFar = nPatchesSoFar + nPatchesInSegment
  if showStats:
    print("prepForKnn: %d segments, %d patches, %.1f seconds, %.1f minutes\n" %\
	    (len(segData), nPatchesSoFar, int(nPatchesSoFar / 10), int(nPatchesSoFar / 600)))
  propsForAllPatches=np.delete(propsForAllPatches,0,axis=0)
  return featuresForAllPatches, propsForAllPatches

#model= makePPM('stance-master/testeng/audio/', 'stance-master/testeng/annotations/', 'stance-master/src/mono4.fss', 'ppmtestpy')
#featuresForAllPatches, propsForAllPatches = prepForKnn(model,3,True)
#scipy.io.savemat('prepforknnpy', {'featuresForAllPatchespy': featuresForAllPatches,'propsForAllPatchespy':propsForAllPatches})  
#   