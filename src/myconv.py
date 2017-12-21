# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 19:11:55 2017

@author: Anindita Nath
University of Texas at ElPaso
"""
import math
import numpy as np
from laplacianOfGaussian import laplacianOfGaussian
from readtracks import readtracks
from computeLogenergy import computeLogEnergy
from lookOrComputePitch import lookupOrComputePitch
from triangleFilter import triangleFilter

#like the standard convolution, except pad with zeros
#to trimwidth at beginning and end, to avoid artifacts

def myconv(vector, filterarray, filterHalfWidth):
    
  if (len(vector)>=len(filterarray)):
     result = np.convolve(vector, filterarray, 'same')
  else:
     result = np.convolve(filterarray,vector, 'same')   
 
  trimWidth = int(math.floor(filterHalfWidth))
  result[:trimWidth] = 0
  result[(len(result) - trimWidth) :] = 0
  #print(result)
  #print(result.shape)     
  return result

#energy=np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])
#[s,c,r] = readtracks('stance-master/testeng/audio/ChevLocalNewsJuly3.au')
#samplesPerFrame = int(10 * int(r / 1000))
#e = computeLogEnergy(s, samplesPerFrame)
#mc=myconv(e,laplacianOfGaussian(6),6*2.5)
#paddedPitch,paddedCenters=lookupOrComputePitch('stance-master/testeng/audio/','ChevLocalNewsJuly3.au','l')
#
#validPitch=(paddedPitch > 0)
#
#mc=myconv(1.0 * validPitch, triangleFilter(160), 10)
#np.set_printoptions(threshold=np.inf)
#print(mc.shape)