# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 19:38:18 2017

@author: Anindita Nath
University of Texas at ElPaso
"""
import math
import numpy as np

#Input is distance, output is nearness
#Distance is in arbitrary units.
#When distance is close to 0, nearness is close to 1
#When distance is large, nearness approaches zero
#This has not been tested in actual use. 
def distanceToNearness(distanceVec):
  nearnessVec = np.divide(1.0,(np.log(np.add(.0001, distanceVec))))
  return nearnessVec

#distanceVec = 456
##distanceVec=np.array([0,0,0,0,np.nan,0,0,0,0,0,0,0.01])
#nearnessVec=distanceToNearness(distanceVec)
#np.set_printoptions(threshold=np.nan)
#print(nearnessVec)
