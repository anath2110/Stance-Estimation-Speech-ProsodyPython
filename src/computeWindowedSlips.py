# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 15:43:08 2017

@author: Anindita Nath
University of Texas at ElPaso
"""

#computeWindowedSlips.m
# converted from original by Nigel Ward, University of Texas at El Paso and Kyoto University
#January 2016

#Computes a smoothed measure of disalignment between pitch and energy peaks,
#that is, the "slip" between the pitch and the energy
#Also includes code for plotting things to see how it's being computed
#NB, unlike all the other mid-level features, this one is almost everywhere
#very near zero
import numpy as np
from epeakness import epeakness
from ppeakness import ppeakness
from misalignment import misalignment
from rectangularFilter import rectangularFilter
from readtracks import readtracks
from computeLogenergy import computeLogEnergy
from lookOrComputePitch import lookupOrComputePitch

def computeWindowedSlips(energy, pitch, duration):
    if (len(energy) == (len(pitch) + 1)):
      #not sure why this sometimes happens, but just patch it
      energy = energy[:len(energy)-1]
      
    elif (len(energy) != len(pitch)):
        
        print('length(energy) is ' +  str(len(energy)))
        print('but length(pitch) is ' +  str(len(pitch)))
          # if a larger discrepancy, can't patch it     
    
    epeaky = epeakness(energy)
    ppeaky = ppeakness(pitch)
      
    misa = misalignment(epeaky, ppeaky)
      
      #useful for interpreting the functions of late pitch peak
      #for dimension-based analysis etc. can comment this out
      #flowtestmisalignment.fss is the minimal fss to get this invoked
      #writeExtremesToFile('highlyMisaligned.txt', misa, 1000 * misa, ...
      #		      'times of high misalignment', ...
      #		      sprintf('%s %s', trackspec.filename, trackspec.side));
    
    smoothed = smooth(misa, rectangularFilter(duration))
      
    #(Implementation note: maybe rewrite the other windowization functions
    #to use convolution like this)
    #This has the same name as the builtin function smooth; risky
    return smoothed

def smooth(signal, filterarray):
  if (len(signal)>=len(filterarray)):
      smoothed = np.convolve(signal, filterarray, 'same')
  else:
      smoothed = np.convolve(filterarray,signal, 'same')
  return smoothed


def zNormalize(signal):
   normalized = signal - np.divide(np.mean(signal),np.std(signal))
   return normalized

#test
#energy=np.array(energy=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])
#[s,c,r] = readtracks('stance-master/testeng/audio/ChevLocalNewsJuly3.au')
#samplesPerFrame = int(10 * int(r / 1000))
#e = computeLogEnergy(s[:], samplesPerFrame)
#paddedPitch,paddedCenters=lookupOrComputePitch('stance-master/testeng/audio/','ChevLocalNewsJuly3.au','l')
#
##pitch=np.array([5,4,3,2,1])
##duration=100
#smoothed=computeWindowedSlips(e, paddedPitch, 100)
#print(smoothed.shape)
