# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 12:14:15 2017

@author: Anindita Nath
University of Texas at El Paso
"""
import numpy as np

def  percentilizePitch(pitchPoints, maxPitch):

#create a percentile vector to use as proxy for pitch values
#instead of each Hz value, use its percentile in the overall distribution
#thus this nonlinearly rescales input the input
#NaNs are preserved
#accepts either a row vector or a column vector; returns a column vector
#converted from code by Nigel Ward and Paola Gallardo, UTEP, February 2014

#the input pitchPoints ranges from 50 to about 515
#(even tho we ask the pitch tracker to compute only up to 500)
# we map any points above 500 to NaN

    rounded = np.around(pitchPoints) # round each value to nearest whole number, but not converted to integer if float
    #print(rounded.shape)
    nanidx=(np.argwhere(np.isnan(rounded)==True))# get the indices for nan values 
    #print(nanidx)
    
    #nanidx=nanidx.reshape(1) # convert to a 1-D array/vector
    nanidx=nanidx.flatten()
    #print(nanidx)
    nonnan_rounded=rounded[np.argwhere(np.isnan(rounded)==False)].astype(int)#slice the array with non-nan indices and convert to perfect ints
    #print(nonnan_rounded)
    
   
   
    
    np.set_printoptions(threshold=np.inf) # print whole arrays
    
    
    #first we build up a histogram of the distribution
    counts = np.zeros(maxPitch)
    counts=counts.astype(int)
    #print(counts)
    #print(counts.shape)
    for i in range (len(nonnan_rounded)):
       pitch = nonnan_rounded[i]
       #print(pitch)
       if pitch < maxPitch: # since numpy arrays index start from 0 and 1 less than the length
        #it's in range and not a NaN
         counts[pitch]= counts[pitch] + 1
         #print(counts)
         #print(counts.shape)
    
    
    cummulativeSum = np.cumsum(counts)
    #print(cummulativeSum)
    mapping = cummulativeSum / cummulativeSum[maxPitch -1]
    #print(mapping)
    percentiles = np.zeros(len(nonnan_rounded),)
    for i in range (len(nonnan_rounded)):
       pitch = nonnan_rounded[i]
       if pitch < maxPitch:
          percentiles[i]= mapping[pitch]
       else:
          percentiles[i]= np.nan
    if(np.any(nanidx==len(pitchPoints)-1)):
         percentiles=np.append(percentiles,np.nan)
         nanidx=nanidx[nanidx!=len(pitchPoints)-1]
         percentiles=np.insert(percentiles,nanidx,np.nan)
    else:
         percentiles=np.insert(percentiles,nanidx,np.nan)
   
    return percentiles
#test case:
#percentiles=percentilizePitch(np.array([np.nan,1.02,2,3.86,1,1,3,1,5,14,2,3,5,6,3,5,7,1,np.nan]), 15)
#print(percentiles)
#print(percentiles.shape)