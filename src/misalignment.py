# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 18:43:52 2017

@author: Anindita Nath
University of Texas at ElPaso
"""

#converted from original by Nigel Ward, UTEP and Kyoto U, January 2016

#inspired by the need to estimate pitch-peak delay, 
#but a much simpler conception: just measure misalignment
#don't worry whether it's pulled forward or back
#because who can tell? without a stressed-syllable oracle
#note that a more traditional, but less reliable, estimator is computeSlip.m

#Note that misalignments are only salient if they come at a peak.
#see also comments in ../sliptest/README.TXT

#note that "misalignment" is a misnomer, since these things are 
#not errors; perhaps "disalignment"
import numpy as np

from rectangularFilter import rectangularFilter
from readtracks import readtracks
from computeLogenergy import computeLogEnergy
from lookOrComputePitch import lookupOrComputePitch
from epeakness import epeakness
from ppeakness import ppeakness

def misalignment(epeaky, ppeaky):

  localMaxEPeak = findLocalMax(epeaky, 120)

  expectedProduct =np.multiply(localMaxEPeak,ppeaky)
  actualProduct = np.multiply(epeaky,ppeaky)

  estimate = np.multiply(np.subtract(expectedProduct,actualProduct),ppeaky)
             
  return estimate
 

#Return a vector where each element e is 
#the max value found a window of size width centered about position e.
#Maybe should have a discount factor for elements further off,
#or otherwise soften the edges of this filter

def findLocalMax(vector, widthMs):
  
  halfwidthFrames = int(int(widthMs / 2) / 10)
  mx = np.zeros(len(vector),)
  for e in range(len(vector)):
     startframe = max(1, e - halfwidthFrames)
     endframe = min(e + halfwidthFrames, len(vector))
     mx[e] =np.amax(vector[startframe:endframe])
     
  return mx

#test with
#mx=findLocalMax(np.array([1,2,3,4,1,2,3,4,1,1,2,4,5,7,1,1,1,1,2]), 60)
#np.set_printoptions(threshold=np.inf)
#print(mx)
#[s,c,r] = readtracks('stance-master/testeng/audio/ChevLocalNewsJuly3.au')
#samplesPerFrame = int(10 * int(r / 1000))
#e = computeLogEnergy(s[:], samplesPerFrame)
#paddedPitch,paddedCenters=lookupOrComputePitch('stance-master/testeng/audio/','ChevLocalNewsJuly3.au','l')
#ep = epeakness(e)
#pp = ppeakness(paddedPitch)
#misa = misalignment(ep, pp)
#print(misa.shape)

   
