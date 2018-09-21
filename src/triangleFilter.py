# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 19:35:04 2017

@author: Anindita Nath
University of Texas at ElPaso
"""
import math
import numpy as np

#returns a filter to be convolved with a pitch-per-frame vector etc.
def  triangleFilter(windowDurationMs):
    
  durationFrames = int(math.floor(windowDurationMs / 10))
  center =int(math.floor(durationFrames / 2)) 
  
  filterarray=np.zeros(durationFrames,)
  
  for i in range(durationFrames):
     filterarray[i] = center - abs(i - (center-1))

  filterarray = np.divide(filterarray,np.sum(filterarray)) #normalize it to sum to one
  return filterarray
#
#tf=triangleFilter(160)
#np.set_printoptions(threshold=np.inf)
#print(tf)