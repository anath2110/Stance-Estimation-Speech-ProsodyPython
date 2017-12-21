# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 17:00:33 2017

@author: Anindita Nath
University ofTexas at El Paso
"""
import numpy as np
def killBleeding(pitchl, pitchr, energyl, energyr):
  
#Nigel Ward, UTEP, 2015
#if the pitch is the same in both tracks, 
#and one track is clearly louder than the other,
#assume bleeding, and set the pitch value in the quieter track value to NaN

#threshold: the min difference in log-energy values between tracks
#to say there's speech in one but not in the other
#This was by looking at 21d.au and trying different thresholds
#In general, this will depend on microphone placements etc.
    clearDifference = 0.8    
        
    #the energy features are centered at 5ms, 15ms, 25ms etc
    #the pitch features are center at 10ms, 20ms, 30ms etc. 
    leftTwentyMsEnergy  = np.add(energyl[:len(energyl)-1],energyr[1:])
    #print(leftTwentyMsEnergy.shape)
    rightTwentyMsEnergy =np.add( energyr[:len(energyr)-1], energyr[1:])
    #print(rightTwentyMsEnergy.shape)   
    leftLouder = leftTwentyMsEnergy > rightTwentyMsEnergy + clearDifference
    rightLouder = rightTwentyMsEnergy > leftTwentyMsEnergy + clearDifference
   
    pitchesSame = (((np.divide(pitchl,pitchr))> .95)) & ((np.divide(pitchl,pitchr) )< 1.05)    
    #print(pitchesSame.shape)   
    pitchesDoubled = (((np.divide(pitchl,pitchr))> .475)) & ((np.divide(pitchl,pitchr) )< .525)    
    #print(pitchesDoubled.shape)   
    pitchesHalved =(((np.divide(pitchl,pitchr))> 1.90)) & ((np.divide(pitchl,pitchr) )< 2.10)    
    #print(pitchesHalved.shape)   
    pitchesSuspect = pitchesSame | pitchesDoubled | pitchesHalved
        
    #note: crashes at this point are often due to stale pitchCache files
    bleedingToLeft = rightLouder & pitchesSuspect
    bleedingToRight = leftLouder & pitchesSuspect
    cleanPitchl = pitchl
    cleanPitchl[bleedingToLeft] = np.nan
    cleanPitchr = pitchr
    cleanPitchr[bleedingToRight] = np.nan
    return cleanPitchl, cleanPitchr

# test data, assuming left speaker is male, right speaker is female,
#and there's bleeding both ways
# and there are randomly NaNs and garbage pitch-points
#rawl    = np.array([ 85,np.nan,90,80,85,30,400,200,200,200,199,np.nan])
#energyl = np.array([5,5,5,5,5,1,1,1,1,1,1,1,1])
#rawr =    np.array([np.nan,np.nan,90,80,85,400,300,199,201,201,199,199])
#energyr = np.array([1,1,1,1,1,1,1,5,5,5,5,5,5])
#[cleanPitchl, cleanPitchr]=killBleeding(rawl, rawr, energyl, energyr)
#np.set_printoptions(threshold=np.nan)
#print(cleanPitchl)
#print(cleanPitchr)