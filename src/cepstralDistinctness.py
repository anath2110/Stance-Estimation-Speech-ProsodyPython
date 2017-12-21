# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 22:18:06 2017

@author: Anindita Nath
University of Texas at ElPaso
"""
import numpy as np
from base import mfcc
from windowize import windowize
import warnings
def cepstralDistinctness(signal, rate, pitch, duration, flag):

  # converted from original by Nigel Ward, January 2017
  # code derived from cepstralFlux.m; see comments there

  #A good measure of phonetic reduction vs enuciation
  # is the degree to which vowels are centralized vs distinct
  # This function measures as a proxy how spectrally close or far from
  #  the average are the voiced segments
  # returns the degree of evidence for reduction or enunciation

  # I'm being here careful to exclude unvoiced segments from consideration
  # tho maybe if I sloppily included them, it wouldn't matter.
  # In dialog, it's probably not common for just one phoneme to be
  #  reduced, so it's probably appropriate to compute these over
  #  no less than a couple of syllables, say 300ms as a minimum window.
  # To make this a better gauge of what''s happing at syllable centers,
  #  could multiply by energy and/or exclude frames without a valid 
  #  pitch point on both sides.

  # This code fails on the Toyota data, producing lots of NaNs; don't know why.

  cc = mfcc(signal, rate, 0.025, 0.01, 13,20,512,300,3700,0.97,22,True,lambda x:np.ones((x,)))
  cc = np.vstack((np.zeros(13,),cc,np.zeros(13,))) # pad, due to the window size
  cct = cc

  nframes = len(pitch)
  #print('nframes' + str(nframes))
  cctlen = len(cct)
  if cctlen - nframes == 2 :
    cct = cct[1:len(cct)-1]  #drop the first point and the last one
  else:
    if cctlen - nframes == 1:
      cct = cct[1:]  # drop the first point 
    else:
      warnings.warn('warning: in cepstralDistinctness')
      print('nframes=%d, cctlen=%d\n', nframes, cctlen);
   
  
  pitchIndices = np.argwhere(~np.isnan(pitch))

  averageCepstrals =np.mean(cct[pitchIndices])
  #print(averageCepstrals.shape)
  repeatedAverages = np.tile(averageCepstrals,(nframes, 1))
  #print(repeatedAverages.shape)
  #print(cct.shape)
  #maybe should square before summing 
  cepstralDistances = np.sum(np.abs(np.subtract(cct,repeatedAverages)),axis=1) 
  #print(cepstralDistances.shape)
  #plotRawCDs(cepstralDistances, pitch, pitchIndices)

  voicedCDs = cepstralDistances[pitchIndices]
  cdAvg = np.mean(voicedCDs)
  cdStdDev = np.std(voicedCDs)

  framevec = np.zeros(nframes,)
  normalizedCDs = (np.subtract(cepstralDistances,cdAvg)) / cdStdDev
  framevec[pitchIndices] = normalizedCDs[pitchIndices]

  pitchValid = ~np.isnan(pitch)
  pitchValidCount = windowize(pitchValid, duration)
  vecSupport = windowize(framevec, duration)
  
  windowVec = np.divide(vecSupport,pitchValidCount)
  windowVec[np.isnan(windowVec)] = 0

  if flag=='enunciation':
    windowVec = np.maximum(windowVec,0) # only care about positive evidence
  elif flag=='reduction':
    windowVec = np.maximum(-windowVec,0) #ditto
  else:
    print('cepstralDistances: ' +  flag)
  return windowVec


 #plot(windowVec)



#tested using validateFeature.m on 21d.au
#Sadly, processing of this audio file seems suffer a lot of bleeding,
#or something: pitch points in the left track where I hear nothing.
#Although when I listen I don't hear much bleeding at all.

#Anyway, the left track, seems generally very enunciated, but
#extra-enunciated sometimes
#and sometimes reduced, e.g.
#at the umms, e.g. 5.5, 19, 61.5, 93
#and at quiet afterthoughts, 25.5, 31.5
#and at discourse markers, 19.4, 81, 115.5
#etc 71.5, 106.5
#examining the 'cd' and 'cb' plots, it generally seems to do well,
#though with a lot of noise ... maybe due to the consonants.

#def plotRawCDs(cepstralDistances, pitch, pitchIndices):
#  clf
#  hold on
#  plot(cepstralDistances);
#  plot(100 + pitch / 10);
#  plot(pitchIndices, cepstralDistances(pitchIndices));
#  legend('cepstralDistances', 'pitch', 'cepstralDistances in voiced regions');
#  ax = gca;
#  ax.XTick = [0:500:12000];

