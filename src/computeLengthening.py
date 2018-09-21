# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 19:38:18 2017

@author: Anindita Nath
University of Texas at ElPaso
"""
import numpy as np
from windowize import windowize
def computeLengthening(relevantEnergy, relevantFlux, duration):

  # converted form original code by Nigel Ward, UTEP, December 2016
  #print(relevantFlux.shape)
  if np.any(relevantFlux==0):
    #replace it with a small value
    minimumvalue=np.amin(relevantFlux[np.where(relevantFlux>0)])
    relevantFlux[np.where(relevantFlux==0)] = minimumvalue
  
  #note that we could instead do relevantEnergy - c1 * relevantFlux,
  #for some constant c1, following Gabriel Skantze's in his Sigdial 2017 paper.
  lengthening = np.divide(relevantEnergy,relevantFlux)

  lengthening[np.isinf(lengthening)] = 0
  lengthening[np.isnan(lengthening)] = 0
  winLengthening = windowize(lengthening, duration)

  return winLengthening

#test cases
#energy=np.array([0,0,0,0,5,5,5,5,4,4,4,4,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,3,3,3,3,5,5,1,0,0,0])
#flux=np.array([0,0,0,0,5,5,5,5,4,4,4,4,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,3,3,3,3,5,5,1,0,0,0])
#duration=100
#winLengthening=computeLengthening(energy, flux, duration)
#np.set_printoptions(threshold=np.nan)
#print(winLengthening)