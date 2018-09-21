# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 20:33:53 2017

@author: Anindita Nath
University of Texas at ElPaso
"""
import math
import numpy as np

def rectangularFilter(windowDurationMs):
  durationFrames = int(math.floor(windowDurationMs / 10))
  filterarray = np.ones(durationFrames,) / durationFrames
  return filterarray

#rf=rectangularFilter(100)
#np.set_printoptions(threshold=np.inf)
#print(rf)